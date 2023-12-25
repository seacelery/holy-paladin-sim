import paladin
import random
import copy
from target import Target, BeaconOfLight, EnemyTarget
from auras_buffs import HolyReverberation, HoT
from misc_functions import append_aura_removed_event, get_timestamp, append_aura_applied_event
import pprint
pp = pprint.PrettyPrinter(width=200)

from misc_functions import format_time


class Simulation:
    
    def __init__(self, paladin, healing_targets_list, encounter_length, priority_list = None):
        self.paladin = paladin
        self.healing_targets_list = healing_targets_list
        self.enemy_targets_list = [EnemyTarget("enemyTarget1")]
        self.encounter_length = encounter_length
        self.elapsed_time = 0
        self.priority_list = priority_list
        # increase tick rate for better hot accuracy
        self.tick_rate = 0.01
        self.abilities = paladin.abilities
        
        self.times_direct_healed = {}
        self.previous_ability = None
                
    def simulate(self):
        while self.elapsed_time < self.encounter_length:
            if self.paladin.currently_casting is not None:
                self.paladin.remaining_cast_time -= self.tick_rate
                if self.paladin.remaining_cast_time <= 0:
                    self.complete_cast(self.paladin, self.elapsed_time)
                    self.paladin.currently_casting = None
                    # self.remove_expired_auras()
            
            if "Divine Resonance" in self.paladin.active_auras:
                self.paladin.active_auras["Divine Resonance"].increment_divine_resonance(self.paladin, self.elapsed_time, self.tick_rate)      
            if "Tyr's Deliverance (self)" in self.paladin.active_auras:
                self.paladin.active_auras["Tyr's Deliverance (self)"].increment_tyrs_deliverance(self.paladin, self.elapsed_time, self.tick_rate)  
            if "Light's Hammer" in self.paladin.active_summons:
                self.paladin.active_summons["Light's Hammer"].increment_lights_hammer(self.paladin, self.elapsed_time, self.tick_rate)
            if "Blessing of Winter" in self.paladin.active_auras:
                self.paladin.active_auras["Blessing of Winter"].increment_blessing_of_winter(self.paladin, self.elapsed_time, self.tick_rate)
            self.action()
            self.paladin.update_gcd(self.tick_rate)
            self.check_delayed_casts(self.paladin)
            self.decrement_cooldowns()
            self.decrement_buffs_on_self()
            self.decrement_buffs_on_targets()
            self.decrement_debuffs_on_targets()
            self.decrement_summons()
            self.increment_rppm_effects()
            self.regen_mana()
            
            self.elapsed_time += self.tick_rate
    
    def check_delayed_casts(self, caster):
        for cast in caster.delayed_casts:
            if self.elapsed_time >= cast[1]:
                glimmer_targets = [glimmer_target for glimmer_target in caster.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
                cast[0].cast_healing_spell(self.paladin, [cast[2]], self.elapsed_time, True, glimmer_targets)
                caster.delayed_casts.remove(cast)
    
    def complete_cast(self, caster, current_time):
        non_beacon_targets = [target for target in self.healing_targets_list if not isinstance(target, BeaconOfLight)]
        
        ability = self.abilities.get(self.paladin.currently_casting)
        if ability:
            # handle divine favor exception: flash of light cast time < global cooldown
            divine_favor_active = False
            if "Divine Favor" in caster.active_auras:
                divine_favor_active = True
            
            if ability.healing_target_count > 1:
                targets = self.choose_multiple_targets(ability, non_beacon_targets)
            else:
                targets = [random.choice(non_beacon_targets)]
            ability.cast_healing_spell(self.paladin, targets, current_time, ability.is_heal)
            
            if ability.calculate_cast_time(caster) * 0.7 < caster.hasted_global_cooldown and divine_favor_active:
                caster.global_cooldown = caster.hasted_global_cooldown - ability.calculate_cast_time(caster) * 0.7
            else:
                caster.global_cooldown = 0
            
    def action(self):
        if self.paladin.currently_casting:
            return
        
        non_beacon_targets = [target for target in self.healing_targets_list if not isinstance(target, BeaconOfLight)]
    
        priority_list = [
            # ("Blessing of the Seasons", lambda: True),
            # ("Avenging Wrath", lambda: True),
            ("Holy Shock", lambda: True),
            ("Light's Hammer", lambda: True),
            # ("Divine Toll", lambda: True),
            # ("Tyr's Deliverance", lambda: True),
            # ("Divine Toll", lambda: self.paladin.holy_power == 4),
            # ("Divine Favor", lambda: True),
            # ("Blessing of Freedom", lambda: True),
            # ("Light of Dawn", lambda: self.paladin.holy_power == 5),
            # ("Holy Shock", lambda: True),
            # ("Light of Dawn", lambda: self.paladin.holy_power == 5),
            # ("Word of Glory", lambda: True),
            # ("Crusader Strike", lambda: True),
            # ("Light of Dawn", lambda: self.paladin.holy_power >= 3),
            
            
            # ("Holy Shock", lambda: "First Light" in self.paladin.active_auras),
            # ("Holy Shock", lambda: 127 <= self.elapsed_time <= 128),
            # ("Daybreak", lambda: 128 <= self.elapsed_time <= 129),
            # ("Holy Shock", lambda: self.elapsed_time <= 2),
            # ("Daybreak", lambda: self.elapsed_time >= 9),
            # ("Divine Toll", lambda: True),
            # ("Holy Shock", lambda: self.elapsed_time >= 10),
            
            # ("Wait", lambda: 2 < self.elapsed_time < 14),
            # ("Holy Shock", lambda: True),
            # # ("Word of Glory", lambda: True),
            # ("Crusader Strike", lambda: True),
            # # ("Flash of Light", lambda: True),
            # # ("Holy Light", lambda: "Divine Favor" in self.paladin.active_auras),
            # # ("Judgment", lambda: "Awakening READY!!!!!!" in self.paladin.active_auras),
            ("Judgment", lambda: True),
            ("Light of Dawn", lambda: True),
            # ("Light of Dawn", lambda: self.paladin.holy_power >= 3),
            # ("Holy Light", lambda: True),
            # ("Divine Toll", lambda: self.elapsed_time >= 10),
        ]  
        
        if self.priority_list:
            priority_list = self.priority_list
        
        for ability_name, condition in priority_list:    
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
                                targets = self.choose_multiple_targets(ability, non_beacon_targets)
                            else:
                                targets = [random.choice(non_beacon_targets)]
                            
                            for target in targets:
                                self.times_direct_healed[target.name] = self.times_direct_healed.get(target.name, 0) + 1
                            
                            # adjust target selection for glimmer of light    
                            if ability.name == "Holy Shock" or ability.name == "Divine Toll" or ability.name == "Daybreak":
                                glimmer_targets = [glimmer_target for glimmer_target in self.healing_targets_list if "Glimmer of Light" in glimmer_target.target_active_buffs]
                                non_glimmer_targets = [glimmer_target for glimmer_target in self.healing_targets_list if "Glimmer of Light" not in glimmer_target.target_active_buffs]
                            
                                # to exclude beacons from holy shock target selection:
                                non_glimmer_non_beacon_targets = [t for t in non_glimmer_targets if t not in self.paladin.beacon_targets] 
                                # if self.holy_shock_target_selection == "Single":
                                # targets = [t for t in non_beacon_targets if t.name == "target18"]
                                # elif self.holy_shock_target_selection == "Multi":
                                targets = [random.choice(non_glimmer_non_beacon_targets)]              
                                # targets = [random.choice(non_glimmer_targets)]
                                ability.cast_healing_spell(self.paladin, targets, self.elapsed_time, ability.is_heal, glimmer_targets)
                            else:
                                ability.cast_healing_spell(self.paladin, targets, self.elapsed_time, ability.is_heal)
                                
                            self.previous_ability = ability.name
                            # print(f"new previous ability: {ability.name}")
                    
                            break
                    # damage spells
                    elif ability.is_damage_spell:
                        targets = [random.choice(self.enemy_targets_list)]
                        ability.cast_damage_spell(self.paladin, targets, self.elapsed_time, non_beacon_targets)
    
    def choose_multiple_targets(self, ability, non_beacon_targets):
        targets = []
                    
        beacon_targets = self.paladin.beacon_targets.copy()
        
        # 3 means beacon targets chosen 15% of the time for some reason i don't really know
        num_beacon_targets = random.choices([0, 1], weights=[1, 3], k=1)[0]
        
        for _ in range(num_beacon_targets):
            beacon_target = random.choice(beacon_targets)
            targets.append(beacon_target)
            beacon_targets.remove(beacon_target)
            
        remaining_targets_count = ability.healing_target_count - len(targets)
        targets.extend(random.sample(non_beacon_targets, min(len(non_beacon_targets), remaining_targets_count)))
        return targets
                    
    def decrement_cooldowns(self):
        for ability_name, ability_instance in self.abilities.items():
            # keep an eye on this v
            # if ability_instance.remaining_cooldown > 0:
                # seal of order 10% cdr for holy power generators, blessing of autumn 30% cdr on all abilities
                if "Blessing of Dusk" in self.paladin.active_auras and ability_name in ["Divine Toll", "Holy Shock", "Crusader Strike", "Judgment", "Hammer of Wrath"] and "Blessing of Autumn" in self.paladin.active_auras and self.paladin.is_talent_active("Seal of Order"):
                    ability_instance.remaining_cooldown -= (self.tick_rate * (1 + 0.1 + 0.3))
                elif "Blessing of Dusk" in self.paladin.active_auras and ability_name in ["Divine Toll", "Holy Shock", "Crusader Strike", "Judgment", "Hammer of Wrath"] and self.paladin.is_talent_active("Seal of Order"):
                    ability_instance.remaining_cooldown -= (self.tick_rate * (1 + 0.1))
                elif "Blessing of Autumn" in self.paladin.active_auras:
                    ability_instance.remaining_cooldown -= (self.tick_rate * (1 + 0.3))
                else:
                    ability_instance.remaining_cooldown -= self.tick_rate
                
                # add a charge and restart cooldown when the cooldown of an ability with charges reaches 0
                if ability_instance.remaining_cooldown <= 0 and ability_instance.current_charges < ability_instance.max_charges:
                    ability_instance.current_charges += 1
                    
                    if ability_instance.current_charges < ability_instance.max_charges:
                        ability_instance.start_cooldown(self.paladin)

                                        
    def decrement_buffs_on_self(self):
        # for buff_name, buff in self.paladin.active_auras.items():
            # print(f"{self.elapsed_time}: buff name: {buff_name}, duration: {buff.duration}, charges: {buff.current_stacks}")
        expired_buffs = []
        for buff_name, buff in self.paladin.active_auras.items():
            buff.duration -= self.tick_rate
            if buff.duration <= 0:
                expired_buffs.append(buff_name)
                  
        for buff_name in expired_buffs:
            append_aura_removed_event(self.paladin.buff_events, buff_name, self.paladin, self.paladin, self.elapsed_time)
            
            if buff_name == "Tyr's Deliverance (self)":
                self.paladin.active_auras["Tyr's Deliverance (self)"].trigger_partial_tick(self.paladin, self.elapsed_time)
                
            self.paladin.active_auras[buff_name].remove_effect(self.paladin)
            del self.paladin.active_auras[buff_name]
            # print(f"new crit %: {self.paladin.crit}")
        
    def decrement_buffs_on_targets(self):
        for target in self.healing_targets_list:
            if "Holy Reverberation" in target.target_active_buffs:
                initial_holy_reverberation_count = len(target.target_active_buffs["Holy Reverberation"])
                first_instance_tick_time = target.target_active_buffs["Holy Reverberation"][0].time_until_next_tick
            elif "Holy Reverberation" not in target.target_active_buffs:
                initial_holy_reverberation_count = 0
            
            for buff_name, buff_instances in list(target.target_active_buffs.items()):
                new_buff_instances = []
                for buff in buff_instances:
                    if isinstance(buff, HoT):
                        buff.update_tick_interval(self.paladin)
                        buff.time_until_next_tick -= self.tick_rate
                        
                        if buff_name == "Holy Reverberation" and first_instance_tick_time <= 0 and target.target_active_buffs["Holy Reverberation"][0].time_until_next_tick <= 0:
                            buff.process_tick(self.paladin, target, self.elapsed_time, buff_instances)
                            # reset the tick timing based on the first instance
                            for instance in target.target_active_buffs["Holy Reverberation"]:
                                instance.time_until_next_tick = instance.base_tick_interval / self.paladin.haste_multiplier
                                instance.previous_tick_time = self.elapsed_time

                    buff.duration -= self.tick_rate
                    if buff.duration > 0:
                        new_buff_instances.append(buff)
                    elif isinstance(buff, HoT) and len(buff_instances) == 1:
                        buff.process_tick(self.paladin, target, self.elapsed_time, buff_instances, is_partial_tick=True)

                if new_buff_instances:
                    target.target_active_buffs[buff_name] = new_buff_instances
                    # if "Holy Reverberation" in target.target_active_buffs:
                    #     self.paladin.events.append(f"{self.elapsed_time}: {len(target.target_active_buffs['Holy Reverberation'])}")
                else:
                    if buff_name in target.target_active_buffs:
                        if "Glimmer of Light" in target.target_active_buffs and buff_name == "Glimmer of Light":
                            target.apply_buff_to_target(HolyReverberation(self.paladin), self.elapsed_time)
                            longest_reverberation_duration = max(buff_instance.duration for buff_instance in target.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in target.target_active_buffs and target.target_active_buffs["Holy Reverberation"] else None
                            if "Holy Reverberation" in target.target_active_buffs:
                                if len(target.target_active_buffs["Holy Reverberation"]) > 0:
                                    self.paladin.buff_events.append(f"{format_time(self.elapsed_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
                        append_aura_removed_event(self.paladin.buff_events, buff_name, self.paladin, target, self.elapsed_time)
                        del target.target_active_buffs[buff_name]
            
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
                        append_aura_removed_event(self.paladin.buff_events, debuff_name, self.paladin, target, self.elapsed_time)
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
    
    def increment_rppm_effects(self):
        if "Touch of Light" in self.paladin.time_since_last_rppm_proc:
            self.paladin.time_since_last_rppm_proc["Touch of Light"] += self.tick_rate
        
    def regen_mana(self):
        if self.paladin.mana + self.paladin.mana_regen_per_second * self.tick_rate > self.paladin.max_mana:
            self.paladin.mana = self.paladin.max_mana
        else:
            self.paladin.mana += self.paladin.mana_regen_per_second * self.tick_rate
    
    def test_healing_and_buff_events(self, target):
        healing_and_buff_events = sorted(self.paladin.events + self.paladin.buff_events, key=get_timestamp)
        pp.pprint(healing_and_buff_events)
        
        return healing_and_buff_events
    
    def test_cast_events(self, target):
        pp.pprint(self.paladin.ability_cast_events)
        return self.paladin.ability_cast_events
        
    def display_results(self, target):
        healing_and_buff_events = sorted(self.paladin.events + self.paladin.buff_events, key=get_timestamp)
        healing_and_beacon_events = sorted(self.paladin.events + self.paladin.beacon_events, key=get_timestamp)
        
        total_healing = 0
        total_healing_no_beacon = 0
        healing_by_target = {}
        for target in self.healing_targets_list:         
            total_healing += target.healing_received
            total_healing_no_beacon += target.healing_received
            healing_by_target[target.name] = target.healing_received
        for beacon_target in self.paladin.beacon_targets:
            total_healing += beacon_target.beacon_healing_received
            healing_by_target[beacon_target.name] = beacon_target.healing_received + beacon_target.beacon_healing_received
        
        print(f"Total healing done: {total_healing}")
        # print(f"Healing by target: {healing_by_target}")
        print(f"Breakdown: {self.paladin.healing_by_ability}")
        
        print(f"Total casts: {self.paladin.total_casts}")
        # print(f"Total crits: {self.paladin.ability_crits}")
        
        # ability_cpm = {}
        # for ability, casts in self.paladin.total_casts.items():
        #     ability_cpm[ability] = casts / (self.encounter_length / 60)
        # print(f"CPM: {ability_cpm}")
        
        
        print(f"Mana remaining: {self.paladin.mana}")
        # print(f"Holy power gained: {self.paladin.holy_power_gained}, Holy power wasted: {self.paladin.holy_power_wasted}")
        # print(f"Sequence: {self.paladin.cast_sequence}")
        # print(f"Healing Sequence: {self.paladin.healing_sequence}")
        
        # DISPLAY DETAILED EVENT OUTPUT
        self.paladin.events.append(f"Total healing w/o beacons: {total_healing_no_beacon}")
        healing_and_buff_events.append(f"Total healing w/o beacons: {total_healing_no_beacon}")
        healing_and_beacon_events.append(f"Total healing: {total_healing}")
        # print()
        # pp.pprint(self.paladin.buff_events)
        # print()
        # pp.pprint(self.paladin.beacon_events)
        # print()
        
        # pp.pprint(self.paladin.events_with_beacon)
        
        # pp.pprint(self.paladin.events)
        pp.pprint(healing_and_buff_events)
        # pp.pprint(healing_and_beacon_events)
        
        # pp.pprint(self.paladin.ability_cast_events)
        
        # this works for a 30s window
        pp.pprint(self.paladin.holy_power_by_ability)
        print(f"Glimmers applied: {self.paladin.glimmer_application_counter}")
        print(f"Glimmers removed: {self.paladin.glimmer_removal_counter}")
        
        # print(f"Direct heals: {self.times_direct_healed}")
        
