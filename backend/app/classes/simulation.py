import random
import pprint
import inspect
import sys
import copy
import time
import cProfile
import json
import eventlet
from flask_socketio import emit

from collections import defaultdict

from .target import Target, BeaconOfLight, EnemyTarget, SmolderingSeedling
from .trinkets import Trinket
from .auras_buffs import HolyReverberation, HoT, BeaconOfLightBuff, AvengingWrathAwakening, AvengingCrusaderAwakening, TimeWarp, BestFriendsWithAerwynEmpowered, BestFriendsWithPipEmpowered, BestFriendsWithUrctosEmpowered, CorruptingRage, RetributionAuraTrigger, LightOfTheMartyrBuff, BestowLight, EternalFlameBuff, InfusionOfLight, SunsAvatarActive, DeliberateIncubation, RecklessIncubation, SavingGraces
from ..utils.misc_functions import append_aura_removed_event, get_timestamp, append_aura_applied_event, format_time, update_self_buff_data, update_target_buff_data, update_mana_gained, handle_flat_cdr
from .priority_list_dsl import parse_condition, condition_to_lambda
from .simulation_state import check_cancellation, reset_simulation

pp = pprint.PrettyPrinter(width=200)


class Simulation:
    
    def __init__(self, paladin, healing_targets_list, encounter_length, iterations, time_warp_time, priority_list, custom_equipment, tick_rate, raid_health, mastery_effectiveness, light_of_dawn_targets, lights_hammer_targets, resplendent_light_targets, dawnlight_targets, suns_avatar_targets, seasons, overhealing, access_token, test=False):

        self.access_token = access_token

        self.paladin = paladin
        self.healing_targets_list = healing_targets_list
        self.enemy_targets_list = [EnemyTarget("enemyTarget1")]
        self.encounter_length = encounter_length
        self.elapsed_time = 0
        self.iterations = 100 if iterations == 101 else iterations
        self.priority_list_text = priority_list
        self.priority_list = []
        self.custom_equipment = custom_equipment
        self.paladin.update_equipment(custom_equipment)
        self.test = test

        for item in priority_list:
            action_name, parsed_conditions = parse_condition(item)
            condition_lambda = condition_to_lambda(self, parsed_conditions)
            self.priority_list.append((action_name, condition_lambda))
            
        self.overhealing = overhealing
        
        # make tick rate smaller for better hot accuracy
        self.tick_rate = float(tick_rate)
        self.abilities = paladin.abilities
        
        self.time_warp_time = time_warp_time
        self.time_warp_recharge_timer = 0
        self.time_warp_recharging = False
        
        self.iced_phial_active = False
        self.iced_phial_timer = 0
        self.saving_graces_timer = 0
        self.light_of_the_martyr_uptime = 0.8
        self.light_of_the_martyr_timer = 0
        self.bestow_light_timer = 0
        self.retribution_aura_timer = 40
        self.source_of_magic_timer = 0
        self.symbol_of_hope_timer = 150 if encounter_length > 210 else 30
        self.mana_spring_totem_timer = 0
        self.mana_tide_totem_timer = 150 if encounter_length > 210 else 30
        
        self.times_direct_healed = {}
        self.previous_ability = None
        
        self.time_since_last_buff_interval = {}
        self.time_since_last_check = 0
        self.previous_total_healing = 0
        self.aura_healing = {}
        self.aura_instances = {}

        self.paladin.set_beacon_targets()

        # apply beacon of light at the start of the simulation
        for target in self.paladin.beacon_targets:
            target.apply_buff_to_target(BeaconOfLightBuff(self.paladin), self.elapsed_time, caster=self.paladin)
        
        self.paladin.average_raid_health_percentage = int(raid_health) / 100
        self.paladin.mastery_effectiveness = int(mastery_effectiveness) / 100
        self.paladin.variable_target_counts["Light of Dawn"] = int(light_of_dawn_targets)
        self.paladin.abilities["Light of Dawn"].healing_target_count = self.paladin.variable_target_counts["Light of Dawn"]
        self.paladin.variable_target_counts["Light's Hammer"] = int(lights_hammer_targets)
        self.paladin.variable_target_counts["Resplendent Light"] = int(resplendent_light_targets)
        self.paladin.variable_target_counts["Dawnlight"] = int(dawnlight_targets)
        self.paladin.variable_target_counts["Sun's Avatar"] = int(suns_avatar_targets)
        self.paladin.seasons = seasons
        
        # testing
        self.test_time_since_last = 0
        
        # the copy is used at the start of each simulation
        self.initial_state = copy.deepcopy(self)
               
    def simulate(self):
        while self.elapsed_time < self.encounter_length:
            self.handle_time_warp()
            self.paladin.check_external_buff_timers(self.elapsed_time)
            self.handle_cast_time_spells()

            self.check_under_20_percent()
                    
            self.increment_effects_with_additional_triggers()
            self.increment_rppm_effects()
            
            self.action()
            self.paladin.update_gcd(self.tick_rate)
            self.check_delayed_casts(self.paladin)
            self.decrement_cooldowns()
            self.decrement_buffs_on_self()
            self.decrement_buffs_on_targets()
            self.decrement_debuffs_on_targets()
            self.decrement_summons()
            self.decrement_trinkets()
            self.increment_time_based_stacking_buffs()
            self.increment_passive_heal_over_time_effects()
            self.regen_mana()
            
            # TESTING ONLY
            self.test_time_since_last += self.tick_rate
            if self.test_time_since_last > 1:
                # print(f"time: {self.elapsed_time}, healing: {self.paladin.healing_multiplier}, crit: {self.paladin.crit}")
                
                # print(f"time: {self.elapsed_time}" )
                # for aura in self.paladin.active_auras:
                #     print(self.elapsed_time, aura, self.paladin.active_auras[aura].duration)
                # pp.pprint(self.paladin.active_auras)
                # self.paladin.print_stats(self.elapsed_time)
                self.test_time_since_last = 0
            
            # for display purposes
            self.time_since_last_check += self.tick_rate
            if self.time_since_last_check >= self.tick_rate:
                self.check_buff_counts()
                self.check_healing()
                self.check_resources()
                
            self.elapsed_time += self.tick_rate
            # print(self.elapsed_time, self.paladin.abilities["Holy Shock"].remaining_cooldown, self.paladin.abilities["Holy Shock"].current_charges)
       
    def check_healing(self):
        total_healing = 0
        for spell in self.paladin.ability_breakdown:
            total_healing += self.paladin.ability_breakdown[spell]["total_healing"]
        
        healing_this_second = total_healing - self.previous_total_healing
        self.previous_total_healing = total_healing
            
        self.paladin.healing_timeline[round(self.elapsed_time, 2)] = healing_this_second
        
        # check healing during specific auras
        auras_to_track = set(["Avenging Wrath", "Avenging Wrath (Awakening)", "Rising Sunlight", "Blessing of Spring"])

        # active_auras is a dictionary with aura names as keys
        active_auras = set(self.paladin.active_auras.keys())

        for aura in auras_to_track:
            is_active = aura in active_auras

            if aura not in self.aura_healing:
                self.aura_healing[aura] = {}

            if aura not in self.aura_instances:
                self.aura_instances[aura] = 0

            last_instance = self.aura_instances[aura]

            # start or continue an aura instance
            if is_active:
                if last_instance not in self.aura_healing[aura] or self.aura_healing[aura][last_instance]["end_time"] is not None:
                    self.aura_instances[aura] += 1
                    self.aura_healing[aura][self.aura_instances[aura]] = {
                        "start_time": round(self.elapsed_time, 2),
                        "end_time": None,
                        "total_healing": 0
                    }
                self.aura_healing[aura][self.aura_instances[aura]]["total_healing"] += round(healing_this_second)

            # end the current aura period
            elif self.aura_healing[aura] and last_instance in self.aura_healing[aura] and \
                    self.aura_healing[aura][last_instance]["end_time"] is None:
                self.aura_healing[aura][last_instance]["end_time"] = round(self.elapsed_time, 2)
        
    def check_resources(self):
        self.paladin.mana_timeline.update({round(self.elapsed_time): self.paladin.mana})
        self.paladin.holy_power_timeline.update({round(self.elapsed_time): self.paladin.holy_power})
    
    def check_buff_counts(self):
        glimmer_count = len([glimmer_target for glimmer_target in self.paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs])
        self.paladin.glimmer_counts.update({round(self.elapsed_time): glimmer_count})
        
        tyrs_count = len([tyrs_target for tyrs_target in self.paladin.potential_healing_targets if "Tyr's Deliverance (target)" in tyrs_target.target_active_buffs])
        self.paladin.tyrs_counts.update({round(self.elapsed_time): tyrs_count})
        
        if "Awakening" in self.paladin.active_auras:
            awakening_count = self.paladin.active_auras["Awakening"].current_stacks
        else:
            awakening_count = 0
        self.paladin.awakening_counts.update({round(self.elapsed_time): awakening_count})
        
        self.time_since_last_check = 0
    
    def check_delayed_casts(self, caster):
        for cast in caster.delayed_casts:
            if self.elapsed_time >= cast[1]:
                glimmer_targets = [glimmer_target for glimmer_target in caster.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
                cast[0].cast_healing_spell(self.paladin, [cast[2]], self.elapsed_time, True, glimmer_targets)
                caster.delayed_casts.remove(cast)
    
    def complete_cast(self, caster, current_time):
        non_beacon_targets = [target for target in self.paladin.potential_healing_targets if "Beacon of Light" not in target.target_active_buffs]
        
        ability = self.abilities.get(self.paladin.currently_casting)
        
        sys.stdout.flush()
        for target in non_beacon_targets:
            if "Tyr's Deliverance (target)" in target.target_active_buffs:
                sys.stdout.flush()
       
        if ability:
            # handle divine favor exception: flash of light cast time < global cooldown
            divine_favor_active = False
            if "Divine Favor" in caster.active_auras:
                divine_favor_active = True
            
            if ability.healing_target_count > 1:
                targets = self.paladin.choose_multiple_targets(ability, non_beacon_targets)
            elif "Smoldering Seedling active" in self.paladin.active_auras:
                smoldering_seedling_target = next((target for target in self.paladin.potential_healing_targets if isinstance(target, SmolderingSeedling)), None)
                targets = [smoldering_seedling_target]
            else:
                targets = [random.choice(non_beacon_targets)]
            
            # precast holy light -> beacon of virtue bug
            if ability.name == "Holy Light" and caster.is_talent_active("Beacon of Virtue"):
                beacon_of_virtue = self.paladin.abilities["Beacon of Virtue"]
                if beacon_of_virtue.remaining_cooldown <= 0 and caster.mana >= beacon_of_virtue.get_mana_cost(self.paladin):
                    for ability_name, condition in self.priority_list:    
                        if ability_name in self.abilities and condition():
                            if ability_name == "Beacon of Virtue":
                                # apply virtue beacons early
                                chosen_target = random.choice(caster.potential_healing_targets)
                                secondary_targets = random.sample([target for target in caster.potential_healing_targets if target != chosen_target], 4)                               
                                caster.beacon_targets = [chosen_target] + secondary_targets                              
                                for target in caster.beacon_targets:
                                    target.apply_buff_to_target(BeaconOfLightBuff(caster), current_time, caster=caster)    
                
            ability.cast_healing_spell(self.paladin, targets, current_time, ability.is_heal)
            
            if ability.calculate_cast_time(caster) * 0.7 < caster.hasted_global_cooldown and divine_favor_active:
                caster.global_cooldown = caster.hasted_global_cooldown - ability.calculate_cast_time(caster) * 0.7
            else:
                caster.global_cooldown = 0
                
            ability.try_trigger_rppm_effects(caster, targets, current_time)
            
            self.previous_ability = ability.name
            
    def action(self):
        if self.paladin.currently_casting:
            return
        
        non_beacon_targets = [target for target in self.paladin.potential_healing_targets if "Beacon of Light" not in target.target_active_buffs]
        
        for ability_name, condition in self.priority_list:    
            if ability_name in self.abilities and condition():
                ability = self.abilities[ability_name]
                if ability.can_cast(self.paladin, self.elapsed_time):                    
                    # healing spells
                    if not ability.is_damage_spell:
                        if ability.base_cast_time > 0 and self.paladin.currently_casting is None:
                            ability.start_cast_time(self.paladin, ability, self.elapsed_time)
                            break
                        else:
                            if ability.healing_target_count > 1:
                                targets = self.paladin.choose_multiple_targets(ability, non_beacon_targets)
                            elif "Smoldering Seedling active" in self.paladin.active_auras:
                                smoldering_seedling_target = next((target for target in self.paladin.potential_healing_targets if isinstance(target, SmolderingSeedling)), None)
                                targets = [smoldering_seedling_target]
                            else:
                                targets = [random.choice(non_beacon_targets)]
                            
                            for target in targets:
                                self.times_direct_healed[target.name] = self.times_direct_healed.get(target.name, 0) + 1
                            
                            # adjust target selection for glimmer of light    
                            if ability.name == "Holy Shock" or ability.name == "Divine Toll" or ability.name == "Daybreak":
                                glimmer_targets = [glimmer_target for glimmer_target in self.paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
                                non_glimmer_targets = [glimmer_target for glimmer_target in self.paladin.potential_healing_targets if "Glimmer of Light" not in glimmer_target.target_active_buffs]
                            
                                # to exclude beacons and/or additional targets from holy shock target selection:                               
                                if self.paladin.is_trinket_equipped("Smoldering Seedling"):
                                    non_glimmer_non_beacon_targets = [
                                                                       t for t in non_glimmer_targets 
                                                                       if t not in self.paladin.beacon_targets 
                                                                       and not isinstance(t, SmolderingSeedling)
                                                                     ]
                                else:
                                    non_glimmer_non_beacon_targets = [t for t in non_glimmer_targets if t not in self.paladin.beacon_targets] 
                                
                                targets = [random.choice(non_glimmer_non_beacon_targets)]              
                                ability.cast_healing_spell(self.paladin, targets, self.elapsed_time, ability.is_heal, glimmer_targets)
                            else:
                                ability.cast_healing_spell(self.paladin, targets, self.elapsed_time, ability.is_heal)
                
                            if not ability.off_gcd:
                                self.previous_ability = ability.name
                            # print(f"new previous ability: {ability.name}")
                    
                            break
                    # damage spells
                    elif ability.is_damage_spell:
                        targets = [random.choice(self.enemy_targets_list)]
                        ability.cast_damage_spell(self.paladin, targets, self.elapsed_time, non_beacon_targets)
                    
    def decrement_cooldowns(self):
        for ability_name, ability_instance in self.abilities.items():
            if ability_instance.remaining_cooldown > 0:
                # seal of order 10% cdr for holy power generators, blessing of autumn 30% cdr on all abilities, avenging crusader 30% cdr for judgment and crusader strike                   
                if "Blessing of Dusk" in self.paladin.active_auras and ability_name in ["Divine Toll", "Holy Shock", "Crusader Strike", "Judgment", "Hammer of Wrath"] and self.paladin.is_talent_active("Seal of Order"):
                    ability_instance.remaining_cooldown -= self.tick_rate * 0.1
                if "Blessing of Autumn" in self.paladin.active_auras and not isinstance(ability_instance, Trinket):
                    ability_instance.remaining_cooldown -= self.tick_rate * 0.3
                if ("Avenging Crusader" in self.paladin.active_auras or "Avenging Crusader (Awakening)" in self.paladin.active_auras) and ability_name in ["Judgment", "Crusader Strike"]:
                    ability_instance.remaining_cooldown -= self.tick_rate * 0.3
                ability_instance.remaining_cooldown -= self.tick_rate
                
                # add a charge and restart cooldown when the cooldown of an ability with charges reaches 0
                if ability_instance.remaining_cooldown <= 0 and ability_instance.current_charges < ability_instance.max_charges:
                    ability_instance.current_charges += 1
                    
                    if ability_instance.current_charges < ability_instance.max_charges:
                        ability_instance.start_cooldown(self.paladin)
                        
    def decrement_trinkets(self):
        for buff_name, buff in self.paladin.active_auras.items():
            if isinstance(buff, (BestFriendsWithPipEmpowered, BestFriendsWithAerwynEmpowered, BestFriendsWithUrctosEmpowered)):
                buff.diminish_effect(self.paladin, self.elapsed_time)
                
    def increment_time_based_stacking_buffs(self):
        if len(self.paladin.time_based_stacking_buffs) > 0:
            for buff, buff_interval in self.paladin.time_based_stacking_buffs.items():
                self.time_since_last_buff_interval[buff.name] = self.time_since_last_buff_interval.get(buff.name, 0)
                self.time_since_last_buff_interval[buff.name] += self.tick_rate
                if self.time_since_last_buff_interval[buff.name] >= buff_interval and buff.current_stacks < buff.max_stacks:
                    self.paladin.apply_buff_to_self(buff, self.elapsed_time, buff.stacks_to_apply, buff.max_stacks)
                    self.time_since_last_buff_interval[buff.name] = 0
                    
    def increment_rppm_effects(self):
        for effect in self.paladin.time_since_last_rppm_proc_attempt:
            self.paladin.time_since_last_rppm_proc_attempt[effect] += self.tick_rate
            self.paladin.time_since_last_rppm_proc[effect] += self.tick_rate
            
        for effect in self.paladin.conditional_effect_cooldowns:
            self.paladin.conditional_effect_cooldowns[effect] -= self.tick_rate
                    
    def increment_passive_heal_over_time_effects(self):
        if self.paladin.is_talent_active("Merciful Auras"):
            merciful_auras = self.paladin.active_auras["Merciful Auras"]
            merciful_auras.timer += self.tick_rate
            
            if merciful_auras.timer >= 2:
                merciful_auras.trigger_passive_heal(self.paladin, self.elapsed_time)
                merciful_auras.timer = 0
                
        if self.paladin.is_talent_active("Saved by the Light"):
            saved_by_the_light = self.paladin.active_auras["Saved by the Light"]
            saved_by_the_light.timer += self.tick_rate
            
            if self.paladin.is_talent_active("Beacon of Virtue"):
                virtue_active = any("Beacon of Light" in target.target_active_buffs for target in self.paladin.potential_healing_targets)
                if saved_by_the_light.timer >= 70 and virtue_active:
                    saved_by_the_light.trigger_passive_heal(self.paladin, self.elapsed_time)
                    saved_by_the_light.timer = 0
            else:
                if saved_by_the_light.timer >= 70:
                    saved_by_the_light.trigger_passive_heal(self.paladin, self.elapsed_time)
                    saved_by_the_light.timer = 0
                    
        if self.paladin.ptr and self.paladin.is_talent_active("Sun's Avatar"):
            if "Avenging Wrath" in self.paladin.active_auras or "Avenging Crusader" in self.paladin.active_auras or "Avenging Wrath (Awakening)" in self.paladin.active_auras or "Avenging Crusader (Awakening)" in self.paladin.active_auras:
                suns_avatar_count = len([target for target in self.paladin.potential_healing_targets if "Sun's Avatar" in target.target_active_buffs])
                target_count = 5 * suns_avatar_count
                
                if suns_avatar_count > 0:
                    suns_avatar = self.paladin.active_auras["Sun's Avatar Active"]
                    suns_avatar.timer += self.tick_rate
                    
                    if suns_avatar.timer >= 0.5:
                        suns_avatar.trigger_passive_heal(self.paladin, self.elapsed_time, target_count)
                        suns_avatar.timer = 0
                        
        if "Ovinax's Mercurial Egg" in self.paladin.trinkets and "Ovinax's Mercurial Egg Paused" not in self.paladin.active_auras:
            option = self.paladin.trinkets.get("Ovinax's Mercurial Egg", {}).get("option")
            ovinaxs_mercurial_egg = self.paladin.active_auras["Ovinax's Mercurial Egg"]
            ovinaxs_mercurial_egg.timer += self.tick_rate
            
            probabilities = {"Low Movement": 0.47, "Some Movement": 0.5, "High Movement": 0.54}
            
            if ovinaxs_mercurial_egg.timer >= 1 and ovinaxs_mercurial_egg.moving:
                if "Deliberate Incubation" in self.paladin.active_auras:
                    self.paladin.active_auras["Deliberate Incubation"].remove_effect(self.paladin)
                    self.paladin.active_auras["Deliberate Incubation"].current_stacks -= 1
                    if self.paladin.active_auras["Deliberate Incubation"].current_stacks == 0:
                        del self.paladin.active_auras["Deliberate Incubation"]
                        update_self_buff_data(self.paladin.self_buff_breakdown, "Deliberate Incubation", self.elapsed_time, "expired")
                    else:
                        self.paladin.active_auras["Deliberate Incubation"].apply_effect(self.paladin)
                    
                    if "Reckless Incubation" in self.paladin.active_auras and self.paladin.active_auras["Reckless Incubation"].current_stacks < 30:
                        self.paladin.active_auras["Reckless Incubation"].remove_effect(self.paladin)
                        self.paladin.active_auras["Reckless Incubation"].current_stacks += 1
                        self.paladin.active_auras["Reckless Incubation"].apply_effect(self.paladin)                  
                    elif "Reckless Incubation" not in self.paladin.active_auras:
                        self.paladin.apply_buff_to_self(RecklessIncubation(self.paladin), self.elapsed_time)
                ovinaxs_mercurial_egg.timer = 0   
                
            if ovinaxs_mercurial_egg.timer >= 1 and not ovinaxs_mercurial_egg.moving:
                if "Reckless Incubation" in self.paladin.active_auras:
                    self.paladin.active_auras["Reckless Incubation"].remove_effect(self.paladin)
                    self.paladin.active_auras["Reckless Incubation"].current_stacks -= 1
                    if self.paladin.active_auras["Reckless Incubation"].current_stacks == 0:
                        del self.paladin.active_auras["Reckless Incubation"]
                        update_self_buff_data(self.paladin.self_buff_breakdown, "Reckless Incubation", self.elapsed_time, "expired")
                    else:
                        self.paladin.active_auras["Reckless Incubation"].apply_effect(self.paladin)
                    
                    if "Deliberate Incubation" in self.paladin.active_auras and self.paladin.active_auras["Deliberate Incubation"].current_stacks < 30:
                        self.paladin.active_auras["Deliberate Incubation"].remove_effect(self.paladin)
                        self.paladin.active_auras["Deliberate Incubation"].current_stacks += 1
                        self.paladin.active_auras["Deliberate Incubation"].apply_effect(self.paladin)                  
                    elif "Deliberate Incubation" not in self.paladin.active_auras:
                        self.paladin.apply_buff_to_self(DeliberateIncubation(self.paladin), self.elapsed_time)
                ovinaxs_mercurial_egg.timer = 0        
            
            random_num = random.random()
            if random_num < probabilities[option]:
                ovinaxs_mercurial_egg.moving = True
            else:
                ovinaxs_mercurial_egg.moving = False
        
    def increment_effects_with_additional_triggers(self):
        if "Divine Resonance" in self.paladin.active_auras:
            self.paladin.active_auras["Divine Resonance"].increment_divine_resonance(self.paladin, self.elapsed_time, self.tick_rate)  
                
        if "Tyr's Deliverance (self)" in self.paladin.active_auras:
            self.paladin.active_auras["Tyr's Deliverance (self)"].increment_tyrs_deliverance(self.paladin, self.elapsed_time, self.tick_rate)  
            
        if "Light's Hammer" in self.paladin.active_summons:
            self.paladin.active_summons["Light's Hammer"].increment_lights_hammer(self.paladin, self.elapsed_time, self.tick_rate)
            
        if "Consecration" in self.paladin.active_summons:
            self.paladin.active_summons["Consecration"].increment_consecration(self.paladin, self.elapsed_time, self.tick_rate)
        for summon_name, summon_instance in self.paladin.active_summons.items():
            if summon_name.startswith("Consecration (Righteous Judgment)"):
                summon_instance.increment_consecration(self.paladin, self.elapsed_time, self.tick_rate)
            
        if "Blessing of Winter" in self.paladin.active_auras:
            self.paladin.active_auras["Blessing of Winter"].increment_blessing_of_winter(self.paladin, self.elapsed_time, self.tick_rate)
            
        if "Iced Phial of Corrupting Rage" in self.paladin.active_auras:
            self.iced_phial_active = True
        if self.iced_phial_active and "Corrupting Rage" not in self.paladin.active_auras:
            self.iced_phial_timer += self.tick_rate
            if self.iced_phial_timer >= 15:
                self.iced_phial_timer = 0
                self.paladin.apply_buff_to_self(CorruptingRage(), self.elapsed_time)
                
        if "Flask of Saving Graces" in self.paladin.active_auras:
            self.saving_graces_timer += self.tick_rate
            if self.saving_graces_timer >= 30:
                self.saving_graces_timer = 0
                self.paladin.apply_buff_to_self(SavingGraces(), self.elapsed_time)
                
        if self.paladin.ptr and self.paladin.is_talent_active("Light of the Martyr"):   
            uptime_duration = self.encounter_length * self.light_of_the_martyr_uptime
            downtime_duration = self.encounter_length - uptime_duration
            light_of_the_martyr_intervals = 5
            
            if self.elapsed_time <= 0.1:
                if "Light of the Martyr" not in self.paladin.active_auras:
                    self.paladin.apply_buff_to_self(LightOfTheMartyrBuff(self.paladin, uptime_duration / light_of_the_martyr_intervals), self.elapsed_time)
                 
            if "Light of the Martyr" in self.paladin.active_auras:
                if self.paladin.is_talent_active("Bestow Light"):
                    if "Bestow Light" not in self.paladin.active_auras:
                        self.bestow_light_timer += self.tick_rate                 
                        if self.bestow_light_timer >= 5:
                            self.paladin.apply_buff_to_self(BestowLight(self.paladin, uptime_duration / light_of_the_martyr_intervals), self.elapsed_time)     
                            if "Bestow Light" in self.time_since_last_buff_interval:
                                self.time_since_last_buff_interval["Bestow Light"] = 0       
                            self.bestow_light_timer = 0  
                
            if "Light of the Martyr" not in self.paladin.active_auras:
                self.light_of_the_martyr_timer += self.tick_rate
                
                if self.light_of_the_martyr_timer >= downtime_duration / light_of_the_martyr_intervals:
                    self.light_of_the_martyr_timer = 0
                    self.paladin.apply_buff_to_self(LightOfTheMartyrBuff(self.paladin, uptime_duration / light_of_the_martyr_intervals), self.elapsed_time)
                    self.bestow_light_timer = 0
                
        if "Retribution Aura " in self.paladin.active_auras:
            self.retribution_aura_timer += self.tick_rate
            if self.retribution_aura_timer >= 45:
                self.retribution_aura_timer = 0
                self.paladin.apply_buff_to_self(RetributionAuraTrigger(), self.elapsed_time)
                
        if "Source of Magic" in self.paladin.active_auras:
            self.source_of_magic_timer += self.tick_rate
            if self.source_of_magic_timer >= 10:
                self.source_of_magic_timer = 0
                source_of_magic_mana_gain = self.paladin.max_mana * 0.0025
                self.paladin.mana += source_of_magic_mana_gain
                update_mana_gained(self.paladin.ability_breakdown, "Source of Magic", source_of_magic_mana_gain)
                
        if "Mana Spring Totem" in self.paladin.active_auras:
            self.mana_spring_totem_timer += self.tick_rate
            if self.mana_spring_totem_timer >= 5.5:
                self.mana_spring_totem_timer = 0
                mana_spring_totem_mana_gain = 150
                self.paladin.mana += mana_spring_totem_mana_gain
                update_mana_gained(self.paladin.ability_breakdown, "Mana Spring Totem", mana_spring_totem_mana_gain)
                
        if "Mana Tide Totem" in self.paladin.active_auras:
            self.mana_tide_totem_timer += self.tick_rate
            if self.mana_tide_totem_timer >= 180:
                self.mana_tide_totem_timer = 0
                mana_tide_totem_mana_gain = 12800
                self.paladin.mana += mana_tide_totem_mana_gain
                update_mana_gained(self.paladin.ability_breakdown, "Mana Tide Totem", mana_tide_totem_mana_gain)
                
        if "Symbol of Hope" in self.paladin.active_auras:
            self.symbol_of_hope_timer += self.tick_rate
            if self.symbol_of_hope_timer >= 180:
                self.symbol_of_hope_timer = 0
                symbol_of_hope_mana_gain = (self.paladin.max_mana - self.paladin.mana) * 0.1
                self.paladin.mana += symbol_of_hope_mana_gain
                update_mana_gained(self.paladin.ability_breakdown, "Symbol of Hope", symbol_of_hope_mana_gain)
                
    def handle_time_warp(self):
        if self.elapsed_time > self.time_warp_time and not self.time_warp_recharging:
            self.paladin.apply_buff_to_self(TimeWarp(), self.elapsed_time)
            self.time_warp_recharging = True
        if self.time_warp_recharging:
            self.time_warp_recharge_timer += self.tick_rate
        if self.time_warp_recharge_timer >= 600:
            self.time_warp_recharge_timer = 0
            self.time_warp_recharging = False
            
    def handle_cast_time_spells(self):
        if self.paladin.currently_casting is not None:
            self.paladin.remaining_cast_time -= self.tick_rate
            if self.paladin.remaining_cast_time <= 0:
                self.complete_cast(self.paladin, self.elapsed_time)
                self.paladin.currently_casting = None
                
    def check_under_20_percent(self):
        if not self.paladin.is_enemy_below_20_percent and self.elapsed_time >= self.encounter_length * 0.8:
            self.paladin.is_enemy_below_20_percent = True   
                                 
    def decrement_buffs_on_self(self):
        expired_buffs = []
        for buff_name, buff in self.paladin.active_auras.items():
            buff.duration -= self.tick_rate
            if buff.duration <= 0:
                expired_buffs.append(buff_name)
                  
        for buff_name in expired_buffs:
            append_aura_removed_event(self.paladin.events, buff_name, self.paladin, self.paladin, self.elapsed_time)
            
            if buff_name == "Tyr's Deliverance (self)":
                self.paladin.active_auras["Tyr's Deliverance (self)"].trigger_partial_tick(self.paladin, self.elapsed_time)
                                  
            if buff_name == "Avenging Wrath" and self.paladin.awakening_queued:
                self.paladin.apply_buff_to_self(AvengingWrathAwakening(), self.elapsed_time)
                self.paladin.awakening_queued = False
                
            if buff_name == "Avenging Crusader" and self.paladin.awakening_queued:
                self.paladin.apply_buff_to_self(AvengingCrusaderAwakening(), self.elapsed_time)
                self.paladin.awakening_queued = False
                
            if self.paladin.ptr and self.paladin.is_talent_active("Laying Down Arms"):    
                if buff_name == "Holy Bulwark" or buff_name == "Sacred Weapon":
                    handle_flat_cdr(self.paladin.abilities["Lay on Hands"], 15)
                    if self.paladin.is_talent_active("Inflorescence of the Sunwell"):
                        self.paladin.apply_buff_to_self(InfusionOfLight(self.paladin), self.elapsed_time, stacks_to_apply=1, max_stacks=2, reapply=True)
                    else:
                        self.paladin.apply_buff_to_self(InfusionOfLight(self.paladin), self.elapsed_time, reapply=True)

            self.paladin.active_auras[buff_name].remove_effect(self.paladin, self.elapsed_time)
            
            if buff_name == "Avenging Wrath" and "Avenging Wrath (Awakening)" in self.paladin.active_auras:
                self.paladin.apply_buff_to_self(SunsAvatarActive(self.paladin), self.elapsed_time)
                
            if buff_name == "Avenging Crusader" and "Avenging Crusader (Awakening)" in self.paladin.active_auras:
                self.paladin.apply_buff_to_self(SunsAvatarActive(self.paladin), self.elapsed_time)
            
            # if the remove effect method refreshes the buff duration, then don't remove it
            if self.paladin.active_auras[buff_name].duration <= 0:
                del self.paladin.active_auras[buff_name]    
                update_self_buff_data(self.paladin.self_buff_breakdown, buff_name, self.elapsed_time, "expired")
        
    def decrement_buffs_on_targets(self):
        for target in self.paladin.potential_healing_targets:            
            if "Holy Reverberation" in target.target_active_buffs:
                initial_holy_reverberation_count = len(target.target_active_buffs["Holy Reverberation"])
                first_instance_tick_time = target.target_active_buffs["Holy Reverberation"][0].time_until_next_tick
            elif "Holy Reverberation" not in target.target_active_buffs:
                initial_holy_reverberation_count = 0
            
            for buff_name, buff_instances in list(target.target_active_buffs.items()):
                new_buff_instances = []
                for buff in buff_instances:
                    if isinstance(buff, HoT):
                        buff.time_until_next_tick -= self.tick_rate
                        
                        # handle specific case of holy reverberation's behaviour
                        if buff_name == "Holy Reverberation" and first_instance_tick_time <= 0 and target.target_active_buffs["Holy Reverberation"][0].time_until_next_tick <= 0:
                            buff.process_tick(self.paladin, target, self.elapsed_time, buff_instances)
                            
                            # reset the tick timing based on the first instance
                            for instance in target.target_active_buffs["Holy Reverberation"]:
                                instance.time_until_next_tick = instance.base_tick_interval / self.paladin.haste_multiplier
                                instance.previous_tick_time = self.elapsed_time
                        
                        # handle regular heal over time effects       
                        elif target.target_active_buffs[buff_name][0].time_until_next_tick <= 0:
                            buff.process_tick(self.paladin, target, self.elapsed_time, buff_instances)
                            buff.previous_tick_time = self.elapsed_time
                            
                            if buff_name == "Holy Reverberation":
                                for instance in target.target_active_buffs["Holy Reverberation"]:
                                    instance.time_until_next_tick = instance.base_tick_interval / self.paladin.haste_multiplier
                                    instance.previous_tick_time = self.elapsed_time
                            elif buff.hasted:
                                buff.time_until_next_tick = buff.base_tick_interval / self.paladin.haste_multiplier
                            else:
                                buff.time_until_next_tick = buff.base_tick_interval
            
                    buff.duration -= self.tick_rate
                    if buff.duration > 0:
                        new_buff_instances.append(buff)
                    elif isinstance(buff, HoT) and len(buff_instances) == 1:
                        buff.process_tick(self.paladin, target, self.elapsed_time, buff_instances, is_partial_tick=True)

                if new_buff_instances:
                    target.target_active_buffs[buff_name] = new_buff_instances
                else:
                    if buff_name in target.target_active_buffs:
                        if "Glimmer of Light" in target.target_active_buffs and buff_name == "Glimmer of Light" and self.paladin.set_bonuses["dragonflight_season_3"] >= 2:
                            target.apply_buff_to_target(HolyReverberation(self.paladin), self.elapsed_time, caster=self.paladin)
                            longest_reverberation_duration = max(buff_instance.duration for buff_instance in target.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in target.target_active_buffs and target.target_active_buffs["Holy Reverberation"] else None
                            if "Holy Reverberation" in target.target_active_buffs:
                                if len(target.target_active_buffs["Holy Reverberation"]) > 0:
                                    self.paladin.events.append(f"{format_time(self.elapsed_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
                        append_aura_removed_event(self.paladin.events, buff_name, self.paladin, target, self.elapsed_time)
                        del target.target_active_buffs[buff_name]
                        
                        if buff_name == "Beacon of Light":
                            self.paladin.beacon_targets.remove(target)
                            
                        if self.paladin.ptr and self.paladin.is_talent_active("Lingering Radiance") and buff_name == "Dawnlight (HoT)":
                            target.apply_buff_to_target(EternalFlameBuff(self.paladin, 10), self.elapsed_time, caster=self.paladin)
                        
                        update_target_buff_data(self.paladin.target_buff_breakdown, buff_name, self.elapsed_time, "expired", target.name)
            
            if "Holy Reverberation" in target.target_active_buffs:
                longest_reverberation_duration = max(buff_instance.duration for buff_instance in target.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in target.target_active_buffs and target.target_active_buffs["Holy Reverberation"] else None            
                if len(target.target_active_buffs["Holy Reverberation"]) < initial_holy_reverberation_count:
                    self.paladin.events.append(f"{format_time(self.elapsed_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) on {target.name}: {round(longest_reverberation_duration, 2)}s remaining")             
    
    def decrement_debuffs_on_targets(self):
        for target in self.enemy_targets_list:
            for debuff_name, debuff_instances in list(target.target_active_debuffs.items()):
                new_debuff_instances = []
                for debuff in debuff_instances:
                    debuff.duration -= self.tick_rate
                    if debuff.duration > 0:
                        new_debuff_instances.append(debuff)

                if new_debuff_instances:
                    target.target_active_debuffs[debuff_name] = new_debuff_instances
                    # if "Holy Reverberation" in target.target_active_buffs:
                    #     self.paladin.events.append(f"{self.elapsed_time}: {len(target.target_active_buffs['Holy Reverberation'])}")
                else:
                    if debuff_name in target.target_active_debuffs:
                        self.paladin.events.append(f"{self.elapsed_time}: {debuff_name} REMOVING")
                        append_aura_removed_event(self.paladin.events, debuff_name, self.paladin, target, self.elapsed_time)
                        del target.target_active_debuffs[debuff_name]
    
    def decrement_summons(self):
        expired_summons = []
        for summon_name, summon in self.paladin.active_summons.items():
            summon.duration -= self.tick_rate
            # this enables the last tick
            if summon.duration <= -0.001:
                expired_summons.append(summon_name)
                  
        for summon_name in expired_summons:
            self.paladin.events.append(f"{format_time(self.elapsed_time)}: {summon_name} ended")
                
            self.paladin.active_summons[summon_name].remove_effect(self.paladin)
            del self.paladin.active_summons[summon_name]
            
            if "Righteous Judgment" in summon_name:
                self.paladin.extra_consecration_count -= 1
        
    def regen_mana(self):
        if self.paladin.mana + self.paladin.mana_regen_per_second * self.tick_rate > self.paladin.max_mana:
            self.paladin.mana = self.paladin.max_mana
        else:
            self.paladin.mana += self.paladin.mana_regen_per_second * self.tick_rate
    
    def update_final_cooldowns_breakdown_times(self):
        for aura, instances in self.aura_healing.items():
                last_instance_number = max(instances.keys(), default=0)
                if last_instance_number > 0:
                    last_instance = instances[last_instance_number]
                    if last_instance["end_time"] is None:
                        last_instance["end_time"] = self.encounter_length
    
    def reset_simulation(self):
        current_state = copy.deepcopy(self.initial_state)
        self.__dict__.update(current_state.__dict__)
    
    def display_results(self):
        print(self.paladin.race)
        print("sp", self.paladin.spell_power)
        print("haste", self.paladin.haste)
        print("crit", self.paladin.crit)
        print("mast", self.paladin.mastery)
        print("vers", self.paladin.versatility)
        
        print(self.paladin.haste_multiplier, self.paladin.crit_multiplier, self.paladin.mastery_multiplier, self.paladin.versatility_multiplier)
        
        full_ability_breakdown_results = {}
        full_self_buff_breakdown_results = {}
        full_target_buff_breakdown_results= {}
        full_aggregated_target_buff_breakdown_results = {}
        full_glimmer_count_results = {}
        full_tyrs_count_results = {}
        full_awakening_count_results = {}
        full_healing_timeline_results = {}
        full_mana_timeline_results = {}
        full_holy_power_timeline_results = {}
        full_cooldowns_breakdown_results = {}
        
        full_awakening_trigger_times_results = {}

        # first spell belongs to the second
        sub_spell_map = {
                "Reclamation (Holy Shock)": "Holy Shock",
                "Reclamation (Crusader Strike)": "Crusader Strike",
                "Divine Revelations (Holy Light)": "Holy Light",
                "Divine Revelations (Judgment)": "Judgment",
                "Holy Shock (Divine Toll)": "Divine Toll",
                "Holy Shock (Divine Resonance)": "Divine Toll",
                "Holy Shock (Rising Sunlight)": "Daybreak",
                "Glimmer of Light": "Holy Shock",
                "Glimmer of Light (Daybreak)": "Daybreak",
                "Glimmer of Light (Rising Sunlight)": "Holy Shock (Rising Sunlight)",
                "Glimmer of Light (Glistening Radiance (Light of Dawn))": "Light of Dawn",
                "Glimmer of Light (Glistening Radiance (Word of Glory))": "Word of Glory",
                "Glimmer of Light (Divine Toll)": "Holy Shock (Divine Toll)",
                "Resplendent Light": "Holy Light",
                "Crusader's Reprieve": "Crusader Strike",
                "Greater Judgment": "Judgment",
                "Judgment of Light": "Judgment",
                "Afterimage": "Word of Glory",
                "Barrier of Faith (Holy Shock)": "Barrier of Faith",
                "Barrier of Faith (Flash of Light)": "Barrier of Faith",
                "Barrier of Faith (Holy Light)": "Barrier of Faith",
                "Blessing of Summer": "Blessing of the Seasons",
                "Blessing of Autumn": "Blessing of the Seasons",
                "Blessing of Winter": "Blessing of the Seasons",
                "Blessing of Spring": "Blessing of the Seasons",
                "Blossom of Amirdrassil Large HoT": "Blossom of Amirdrassil",
                "Blossom of Amirdrassil Small HoT": "Blossom of Amirdrassil",
                "Blossom of Amirdrassil Absorb": "Blossom of Amirdrassil",
                "Veneration": "Hammer of Wrath",
                "Golden Path": "Consecration",
                "Seal of Mercy": "Consecration",
                "Avenging Crusader (Judgment)": "Avenging Crusader",
                "Avenging Crusader (Crusader Strike)": "Avenging Crusader",
                "Dawnlight (HoT)": "Dawnlight",
                "Dawnlight (AoE)": "Dawnlight"
            }

        # time the function
        start_time = time.time()
        
        # complete all simulation iterations and process the data of each
        for i in range(self.iterations):
            if check_cancellation():
                reset_simulation()
                return
            
            # reset simulation states
            print(i)
            if not self.test:
                emit("iteration_update", {"iteration": i + 1}, broadcast=True, namespace="/")
                self.paladin.reset_state()
                self.reset_simulation()
                self.paladin.apply_consumables()
                self.paladin.apply_item_effects()
                self.paladin.apply_buffs_on_encounter_start()
                
            eventlet.sleep(0)
            
            # only record some data on the last iteration
            if i == self.iterations - 1:
                self.paladin.last_iteration = True
                
            self.simulate()
            
            self.update_final_cooldowns_breakdown_times()
            
            ability_breakdown = self.paladin.ability_breakdown
            self_buff_breakdown = self.paladin.self_buff_breakdown
            target_buff_breakdown = self.paladin.target_buff_breakdown
            glimmer_counts = self.paladin.glimmer_counts
            tyrs_counts = self.paladin.tyrs_counts
            awakening_counts = self.paladin.awakening_counts
            healing_timeline = self.paladin.healing_timeline
            mana_timeline = self.paladin.mana_timeline
            holy_power_timeline = self.paladin.holy_power_timeline
            cooldowns_breakdown = self.aura_healing
            
            # accumulate cooldown breakdown results
            for aura, instances in cooldowns_breakdown.items():
                for instance_number, data in instances.items():
                    if aura not in full_cooldowns_breakdown_results:
                        full_cooldowns_breakdown_results[aura] = {}
                    if instance_number not in full_cooldowns_breakdown_results[aura]:
                        full_cooldowns_breakdown_results[aura][instance_number] = {"total_healing": 0, "total_duration": 0, "start_time": 0, "end_time": 0, "count": 0}

                    full_cooldowns_breakdown_results[aura][instance_number]["total_healing"] += data["total_healing"]
                    full_cooldowns_breakdown_results[aura][instance_number]["count"] += 1

                    if data["end_time"] is not None and data["start_time"] is not None:
                        duration = data["end_time"] - data["start_time"]
                        full_cooldowns_breakdown_results[aura][instance_number]["total_duration"] += duration
                        full_cooldowns_breakdown_results[aura][instance_number]["start_time"] += data["start_time"]
                        full_cooldowns_breakdown_results[aura][instance_number]["end_time"] += data["end_time"]
            
            # accumulate awakening trigger results
            for key, value in self.paladin.awakening_trigger_times.items():
                full_awakening_trigger_times_results[key] = full_awakening_trigger_times_results.get(key, 0) + value
            
            # PROCESS ABILITY HEALING
            def add_sub_spell_healing(primary_spell_data):
                total_healing = primary_spell_data.get("total_healing", 0)

                for sub_spell_name, sub_spell_data in primary_spell_data.get('sub_spells', {}).items():
                    total_healing += sub_spell_data.get("total_healing", 0)
                    
                    # add healing and hits from nested sub-spells
                    for nested_sub_spell_data in sub_spell_data.get("sub_spells", {}).values():
                        total_healing += nested_sub_spell_data.get("total_healing", 0)

                return total_healing
            
            def combine_beacon_sources_by_prefix(prefix, beacon_sources):
                combined_source = {
                    "healing": 0,
                    "hits": 0
                }
                keys_to_delete = []

                for spell, data in beacon_sources.items():
                    if spell.startswith(prefix):
                        combined_source["healing"] += data["healing"]
                        combined_source["hits"] += data["hits"]
                        keys_to_delete.append(spell)

                for key in keys_to_delete:
                    del beacon_sources[key]

                beacon_sources[prefix] = combined_source
            
            def add_spell_if_sub_spell_but_no_casts(main_spell, sub_spell):
                if sub_spell in ability_breakdown and main_spell not in ability_breakdown:
                    ability_breakdown[main_spell] = {
                        "total_healing": 0,
                        "casts": 0,
                        "hits": 0,
                        "targets": {},
                        "crits": 0,
                        "mana_spent": 0,
                        "mana_gained": 0,
                        "holy_power_gained": 0,
                        "holy_power_spent": 0,
                        "holy_power_wasted": 0,
                        "sub_spells": {},
                        "source_spells": {}
                    } 
                
            add_spell_if_sub_spell_but_no_casts("Consecration", "Golden Path")
            add_spell_if_sub_spell_but_no_casts("Dawnlight", "Dawnlight (HoT)")
            add_spell_if_sub_spell_but_no_casts("Avenging Crusader", "Avenging Crusader (Judgment)")
            add_spell_if_sub_spell_but_no_casts("Avenging Crusader", "Avenging Crusader (Crusader Strike)")
            
            # process data to include crit percent
            for spell, data in ability_breakdown.items():
                if data["hits"] > data["casts"]:
                    data["crit_percent"] = round((data["crits"] / data["hits"]) * 100, 1)
                else:
                    data["crit_percent"] = round((data["crits"] / data["casts"]) * 100, 1) if data["casts"] > 0 else 0
                        
                for target, target_data in data["targets"].items():
                    target_data["crit_percent"] = round((target_data["crits"] / target_data["casts"]) * 100, 1) if target_data["casts"] > 0 else 0
            
            # assign sub-spell data to primary spell
            for spell, data in ability_breakdown.items():
                if spell in sub_spell_map:
                    primary_spell = sub_spell_map[spell]
                    ability_breakdown[primary_spell]["sub_spells"][spell] = data
            
            for primary_spell, primary_data in ability_breakdown.items():
                if primary_spell in sub_spell_map.values():
                    # add sub-spell healing to the primary spell's healing
                    primary_data["total_healing"] = add_sub_spell_healing(primary_data)
                    
                    # total crits and hits required for crit percent calculation  
                    total_crits = primary_data.get("crits", 0)
                    total_hits = primary_data.get("hits", 0)
                    total_mana_gained = primary_data.get("mana_gained", 0)
                    total_holy_power_gained = primary_data.get("holy_power_gained", 0)
                    total_holy_power_wasted = primary_data.get("holy_power_wasted", 0)
                    if primary_spell == "Blessing of the Seasons":
                        total_mana_spent = primary_data.get("mana_spent", 0)
                        total_casts = primary_data.get("casts", 0)

                    for sub_spell_data in primary_data.get("sub_spells", {}).values():
                        total_crits += sub_spell_data.get("crits", 0)
                        total_hits += sub_spell_data.get("hits", 0)
                        total_mana_gained += sub_spell_data.get("mana_gained", 0)
                        total_holy_power_gained += sub_spell_data.get("holy_power_gained", 0)
                        total_holy_power_wasted += sub_spell_data.get("holy_power_wasted", 0)
                        if primary_spell == "Blessing of the Seasons":
                            total_mana_spent += sub_spell_data.get("mana_spent", 0)
                            total_casts += sub_spell_data.get("casts", 0)

                        for nested_sub_spell_data in sub_spell_data.get("sub_spells", {}).values():
                            total_crits += nested_sub_spell_data.get("crits", 0)
                            total_hits += nested_sub_spell_data.get("hits", 0)
                            total_mana_gained += nested_sub_spell_data.get("mana_gained", 0)
                            total_holy_power_gained += nested_sub_spell_data.get("holy_power_gained", 0)
                            total_holy_power_wasted += nested_sub_spell_data.get("holy_power_wasted", 0)
                        
                    # display holy power for a spell as the sum of its sub-spells
                    primary_data["mana_gained"] = total_mana_gained
                    primary_data["holy_power_gained"] = total_holy_power_gained
                    primary_data["holy_power_wasted"] = total_holy_power_wasted
                    if primary_spell == "Blessing of the Seasons":
                        primary_data["mana_spent"] = total_mana_spent
                        primary_data["casts"] = total_casts
                    
                    # this line is responsible for whether the crit percent propagates back up the table
                    # primary_data["crit_percent"] = round((total_crits / total_hits) * 100, 1) if total_hits > 0 else 0
            
            # remove the primary spell data for sub-spells        
            for spell in [
                "Holy Shock (Divine Toll)", "Holy Shock (Divine Resonance)", "Holy Shock (Rising Sunlight)" , "Glimmer of Light", 
                "Glimmer of Light (Daybreak)", "Glimmer of Light (Rising Sunlight)", "Glimmer of Light (Divine Toll)", 
                "Glimmer of Light (Glistening Radiance (Light of Dawn))", "Glimmer of Light (Glistening Radiance (Word of Glory))", 
                "Resplendent Light", "Greater Judgment", "Judgment of Light", "Crusader's Reprieve", "Afterimage", "Reclamation (Holy Shock)", 
                "Reclamation (Crusader Strike)", "Divine Revelations (Holy Light)", "Divine Revelations (Judgment)", "Blessing of Summer", 
                "Blessing of Autumn", "Blessing of Winter", "Blessing of Spring", "Blossom of Amirdrassil Absorb", "Blossom of Amirdrassil Large HoT", 
                "Blossom of Amirdrassil Small HoT", "Barrier of Faith (Holy Shock)", "Barrier of Faith (Flash of Light)", "Barrier of Faith (Holy Light)", 
                "Veneration", "Golden Path", "Seal of Mercy", "Avenging Crusader (Judgment)", "Avenging Crusader (Crusader Strike)",
                "Dawnlight (HoT)", "Dawnlight (AoE)"
                ]:
                if spell in ability_breakdown:
                    del ability_breakdown[spell]
                          
            # combine beacon glimmer sources into one spell
            if "Beacon of Light" in ability_breakdown:
                beacon_source_spells = ability_breakdown["Beacon of Light"]["source_spells"]   
                combine_beacon_sources_by_prefix("Glimmer of Light", beacon_source_spells)
                combine_beacon_sources_by_prefix("Holy Shock", beacon_source_spells)
            
            excluded_spells = ["Divine Toll", "Daybreak", "Judgment", "Crusader Strike"]
            
            for spell in ability_breakdown:
                if spell not in excluded_spells:
                    total_sub_spell_healing = 0
                    sub_spells = ability_breakdown[spell]["sub_spells"]
                    
                    for sub_spell in sub_spells:
                        total_sub_spell_healing += sub_spells[sub_spell]["total_healing"]
                    
                    if total_sub_spell_healing > 0:   
                        sub_spells[spell] = {
                            "total_healing": 0,
                            "casts": 0,
                            "hits": 0,
                            "targets": {},
                            "crits": 0,
                            "mana_spent": 0,
                            "mana_gained": 0,
                            "holy_power_gained": 0,
                            "holy_power_spent": 0,
                            "holy_power_wasted": 0,
                            "sub_spells": {}
                        }
                        
                        sub_spells[spell]["total_healing"] = ability_breakdown[spell]["total_healing"] - total_sub_spell_healing
                        sub_spells[spell]["casts"] = ability_breakdown[spell]["casts"]
                        sub_spells[spell]["hits"] = ability_breakdown[spell]["hits"]
                        sub_spells[spell]["targets"] = ability_breakdown[spell]["targets"]
                        sub_spells[spell]["crits"] = ability_breakdown[spell]["crits"]
                        sub_spells[spell]["crit_percent"] = ability_breakdown[spell]["crit_percent"]
                        sub_spells[spell]["mana_spent"] = ability_breakdown[spell]["mana_spent"]
                        sub_spells[spell]["mana_gained"] = ability_breakdown[spell]["mana_gained"]
                        sub_spells[spell]["holy_power_gained"] = ability_breakdown[spell]["holy_power_gained"]
                        sub_spells[spell]["holy_power_spent"] = ability_breakdown[spell]["holy_power_spent"]
                        sub_spells[spell]["holy_power_wasted"] = ability_breakdown[spell]["holy_power_wasted"]
            
            for spell in ability_breakdown:
                total_sub_sub_spell_healing = 0
                sub_spells = ability_breakdown[spell]["sub_spells"]
                
                for sub_spell in sub_spells:
                    sub_sub_spells = sub_spells[sub_spell]["sub_spells"]
                    if len(sub_sub_spells) > 0:
                        for sub_sub_spell in sub_sub_spells:
                            total_sub_sub_spell_healing += sub_sub_spells[sub_sub_spell]["total_healing"]      
                            
                        if total_sub_spell_healing > 0:   
                            sub_sub_spells[sub_spell] = {
                                "total_healing": 0,
                                "casts": 0,
                                "hits": 0,
                                "targets": {},
                                "crits": 0,
                                "mana_spent": 0,
                                "mana_gained": 0,
                                "holy_power_gained": 0,
                                "holy_power_spent": 0,
                                "holy_power_wasted": 0,
                                "sub_spells": {}
                            }
                            
                            sub_sub_spells[sub_spell]["total_healing"] = sub_spells[sub_spell]["total_healing"] - total_sub_sub_spell_healing
                            sub_sub_spells[sub_spell]["casts"] = sub_spells[sub_spell]["casts"]
                            sub_sub_spells[sub_spell]["hits"] = sub_spells[sub_spell]["hits"]
                            sub_sub_spells[sub_spell]["targets"] = sub_spells[sub_spell]["targets"]
                            sub_sub_spells[sub_spell]["crits"] = sub_spells[sub_spell]["crits"]
                            sub_sub_spells[sub_spell]["crit_percent"] = sub_spells[sub_spell]["crit_percent"]
                            sub_sub_spells[sub_spell]["mana_spent"] = sub_spells[sub_spell]["mana_spent"]
                            sub_sub_spells[sub_spell]["mana_gained"] = sub_spells[sub_spell]["mana_gained"]
                            sub_sub_spells[sub_spell]["holy_power_gained"] = sub_spells[sub_spell]["holy_power_gained"]
                            sub_sub_spells[sub_spell]["holy_power_spent"] = sub_spells[sub_spell]["holy_power_spent"]
                            sub_sub_spells[sub_spell]["holy_power_wasted"] = sub_spells[sub_spell]["holy_power_wasted"]
            
            # remove spells that aren't actually spells but have subspells               
            for spell in ["Blossom of Amirdrassil", "Hammer of Wrath", "Consecration", "Avenging Crusader", "Dawnlight"]:
                if spell in ability_breakdown:
                    if spell in ability_breakdown[spell]["sub_spells"]:
                        del ability_breakdown[spell]["sub_spells"][spell]
            
            # PROCESS BUFFS                
            def process_buff_data(events):
                def add_time(buff_name, time):
                    if buff_name in buff_summary:
                        buff_summary[buff_name]["total_duration"] += time
                        buff_summary[buff_name]["uptime"] += time / self.encounter_length
                        buff_summary[buff_name]["count"] += 1
                    else:
                        buff_summary[buff_name] = {"total_duration": time, "uptime": time / self.encounter_length, "count": 1, "average_duration": 0}
                
                buff_summary = {}
                active_buffs = {}
                
                for event in events:
                    buff_name = event["buff_name"]
                    event_time = event["time"]
                    event_type = event["type"]
                    
                    if event_type == "applied":
                        if buff_name in active_buffs:
                            active_duration = event_time - active_buffs.pop(buff_name)
                            add_time(buff_name, active_duration)
                            active_buffs[buff_name] = event_time
                        else:
                            active_buffs[buff_name] = event_time
                    elif event_type == "expired":
                        if buff_name in active_buffs:
                            active_duration = event_time - active_buffs.pop(buff_name)
                            add_time(buff_name, active_duration)
                       
                for buff_name, start_time in active_buffs.items():
                    active_duration = self.encounter_length - start_time
                    add_time(buff_name, active_duration)

                for buff in buff_summary:
                    buff_summary[buff]["average_duration"] = buff_summary[buff]["total_duration"] / buff_summary[buff]["count"]
                
                return buff_summary
            
            # include targets separately
            def process_target_buff_data(events):
                def add_time(buff_name, target, time):
                    if buff_name not in buff_summary:
                        buff_summary[buff_name] = {}
                    if target not in buff_summary[buff_name]:
                        buff_summary[buff_name][target] = {
                            "total_duration": 0, 
                            "uptime": 0, 
                            "count": 0, 
                            "average_duration": 0
                        }
                    buff_summary[buff_name][target]["total_duration"] += time
                    buff_summary[buff_name][target]["uptime"] += time / self.encounter_length
                    buff_summary[buff_name][target]["count"] += 1

                buff_summary = {}
                active_buffs = {}

                for event in events:
                    buff_name = event["buff_name"]
                    target = event["target"]
                    event_time = event["time"]
                    event_type = event["type"]
                    key = (buff_name, target)

                    if event_type == "applied":
                        if key in active_buffs:
                            active_duration = event_time - active_buffs.pop(key)
                            add_time(buff_name, target, active_duration)
                        active_buffs[key] = event_time
                    elif event_type == "expired":
                        if key in active_buffs:
                            active_duration = event_time - active_buffs.pop(key)
                            add_time(buff_name, target, active_duration)

                for key, start_time in active_buffs.items():
                    buff_name, target = key
                    active_duration = self.encounter_length - start_time
                    add_time(buff_name, target, active_duration)

                for buff_name in buff_summary:
                    for target in buff_summary[buff_name]:
                        buff_data = buff_summary[buff_name][target]
                        buff_data["average_duration"] = buff_data["total_duration"] / buff_data["count"]

                return buff_summary
            
            # include all targets combined
            def process_aggregated_target_buff_data(events):
                def add_time(buff_name, time):
                    if buff_name in buff_summary:
                        buff_summary[buff_name]["total_duration"] += time
                        buff_summary[buff_name]["uptime"] += time / self.encounter_length
                        buff_summary[buff_name]["count"] += 1
                    else:
                        buff_summary[buff_name] = {"total_duration": time, "uptime": time / self.encounter_length, "count": 1, "average_duration": 0}
                
                buff_summary = {}
                active_buffs = {}
                
                for event in events:
                    buff_name = event["buff_name"]
                    event_time = event["time"]
                    event_type = event["type"]
                    target = event["target"]
                    
                    if event_type == "applied":
                        if buff_name in active_buffs:
                            active_duration = event_time - active_buffs.pop(buff_name)[0]
                            add_time(buff_name, active_duration)
                            active_buffs[buff_name] = [event_time, target]
                        else:
                            active_buffs[buff_name] = [event_time, target]
                    elif event_type == "expired":
                        if buff_name in active_buffs:
                            if target in active_buffs[buff_name]:
                                active_duration = event_time - active_buffs.pop(buff_name)[0]
                                add_time(buff_name, active_duration)
                           
                for buff_name, start_time in active_buffs.items():
                    active_duration = self.encounter_length - start_time[0]
                    add_time(buff_name, active_duration)

                for buff in buff_summary:
                    buff_summary[buff]["average_duration"] = buff_summary[buff]["total_duration"] / buff_summary[buff]["count"]
                
                return buff_summary
            
            # COLLECT RESULTS FOR ALL ITERATIONS
            full_ability_breakdown_results.update({f"iteration {i}": ability_breakdown})
            
            self_buff_summary = process_buff_data(self_buff_breakdown)
            full_self_buff_breakdown_results.update({f"iteration {i}": self_buff_summary})
            
            target_buff_summary = process_target_buff_data(target_buff_breakdown)
            full_target_buff_breakdown_results.update({f"iteration {i}": target_buff_summary})
            
            aggregated_target_buff_summary = process_aggregated_target_buff_data(target_buff_breakdown)
            full_aggregated_target_buff_breakdown_results.update({f"iteration {i}": aggregated_target_buff_summary})
            
            full_glimmer_count_results.update({f"iteration {i}": glimmer_counts})
            full_tyrs_count_results.update({f"iteration {i}": tyrs_counts})
            full_awakening_count_results.update({f"iteration {i}": awakening_counts})
            
            full_healing_timeline_results.update({f"iteration {i}": healing_timeline})
            full_mana_timeline_results.update({f"iteration {i}": mana_timeline})
            full_holy_power_timeline_results.update({f"iteration {i}": holy_power_timeline})
        
        # COMBINE AND AVERAGE ALL KEYS OVER ITERATIONS       
        def combine_results(*dicts):
            def add_dicts(d1, d2):
                for key in d2:
                    if key in d1:
                        if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                            add_dicts(d1[key], d2[key])
                        elif isinstance(d1[key], (int, float)) and isinstance(d2[key], (int, float)):
                            d1[key] += d2[key]
                    else:
                        d1[key] = d2[key]

            combined_results = {}
            for d in dicts:
                add_dicts(combined_results, d)
            return combined_results
        
        def get_all_iterations_results(full_ability_breakdown_results):
            iteration_results = [value for key, value in full_ability_breakdown_results.items() if key.startswith("iteration")]
            return iteration_results

        def average_out_simulation_results(simulation_results, iterations):
            for key in simulation_results:
                if isinstance(simulation_results[key], dict):
                    average_out_simulation_results(simulation_results[key], iterations)
                elif isinstance(simulation_results[key], (int, float)):
                    simulation_results[key] /= iterations
                    
            return simulation_results
        
        def return_complete_combined_results(full_results):
            all_iteration_results = get_all_iterations_results(full_results)
            combined_results = combine_results(*all_iteration_results)
            return average_out_simulation_results(combined_results, self.iterations)
            
        average_ability_breakdown = return_complete_combined_results(full_ability_breakdown_results)
        average_self_buff_breakdown = return_complete_combined_results(full_self_buff_breakdown_results)
        average_target_buff_breakdown = return_complete_combined_results(full_target_buff_breakdown_results)
        average_aggregated_target_buff_breakdown = return_complete_combined_results(full_aggregated_target_buff_breakdown_results)
        average_glimmer_counts = return_complete_combined_results(full_glimmer_count_results)
        average_tyrs_counts = return_complete_combined_results(full_tyrs_count_results)
        average_awakening_counts = return_complete_combined_results(full_awakening_count_results)
        average_healing_timeline = return_complete_combined_results(full_healing_timeline_results)
        average_mana_timeline = return_complete_combined_results(full_mana_timeline_results)
        average_holy_power_timeline = return_complete_combined_results(full_holy_power_timeline_results)
        
        # calculate average hps
        total_healing = 0
        for ability in average_ability_breakdown:
            total_healing += average_ability_breakdown[ability]["total_healing"]
        average_hps = total_healing / self.encounter_length
        
        # adjust cooldowns breakdown for number of iterations
        for aura, instances in full_cooldowns_breakdown_results.items():
            for instance, details in instances.items():
                details["total_duration"] /= details["count"]
                details["total_healing"] /= details["count"]
                details["hps"] = details["total_healing"] / details["total_duration"]
                details["start_time"] /= details["count"]
                details["end_time"] /= details["count"]
        
        # adjust healing timeline from tick rate increments to integers
        adjusted_average_healing_timeline = {}        
        for timestamp, healing in average_healing_timeline.items():
            rounded_time = int(timestamp)
            adjusted_average_healing_timeline[rounded_time] = adjusted_average_healing_timeline.get(rounded_time, 0) + healing
        
        full_results = {
            "healing_timeline": adjusted_average_healing_timeline,
            "mana_timeline": average_mana_timeline,
            "holy_power_timeline": average_holy_power_timeline,
            "ability_breakdown": average_ability_breakdown,
            "self_buff_breakdown": average_self_buff_breakdown,
            "target_buff_breakdown": average_target_buff_breakdown,
            "aggregated_target_buff_breakdown": average_aggregated_target_buff_breakdown,
            "glimmer_counts": average_glimmer_counts,
            "tyrs_counts": average_tyrs_counts,
            "awakening_counts": average_awakening_counts,
            "awakening_triggers": full_awakening_trigger_times_results,
            "priority_breakdown": self.paladin.priority_breakdown,
            "cooldowns_breakdown": full_cooldowns_breakdown_results
        }
        
        simulation_details = {
            "encounter_length": self.encounter_length,
            "paladin_name": self.paladin.name,
            "iterations": self.iterations,
            "max_mana": self.paladin.max_mana,
            "average_hps": average_hps,
            "equipment": self.paladin.equipment,
            # "stats": self.paladin.stats_after_buffs
            "stats": {"haste": round(self.paladin.haste_rating), "crit": round(self.paladin.crit_rating), "mastery": round(self.paladin.mastery_rating), "versatility": round(self.paladin.versatility_rating), 
                  "intellect": round(self.paladin.spell_power), "health": round(self.paladin.max_health), "leech": round(self.paladin.leech_rating), "mana": round(self.paladin.max_mana),
                  "haste_percent": round(self.paladin.haste, 2), "crit_percent": round(self.paladin.crit, 2), "mastery_percent": round(self.paladin.mastery, 2), 
                  "versatility_percent": round(self.paladin.versatility, 2), "leech_percent": round(self.paladin.leech, 2)},
            "talents": {"class_talents": self.paladin.class_talents, "spec_talents": self.paladin.spec_talents},
            "priority_list": self.priority_list_text
        }
    
        end_time = time.time()
        simulation_time = end_time - start_time
        print(f"Simulation time: {simulation_time} seconds")

        if not self.test:
            emit("simulation_complete", {"results": full_results, "simulation_details": simulation_details}, broadcast=True, namespace="/")
        return {"results": full_results, "simulation_details": simulation_details}
