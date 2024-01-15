import random
import pprint
import inspect
import sys
import copy
import time
import cProfile
from flask_socketio import emit

from collections import defaultdict

from .target import Target, BeaconOfLight, EnemyTarget
from .auras_buffs import HolyReverberation, HoT
from ..utils.misc_functions import append_aura_removed_event, get_timestamp, append_aura_applied_event, format_time, update_self_buff_data, update_target_buff_data
from ..utils.battlenet_api import get_spell_icon_data, get_access_token
from ..utils import cache

pp = pprint.PrettyPrinter(width=200)


class Simulation:
    
    def __init__(self, paladin, healing_targets_list, encounter_length, iterations, access_token, priority_list=None):

        self.paladin = paladin
        self.healing_targets_list = healing_targets_list
        self.enemy_targets_list = [EnemyTarget("enemyTarget1")]
        self.encounter_length = encounter_length
        self.elapsed_time = 0
        self.iterations = iterations
        self.priority_list = priority_list
        # increase tick rate for better hot accuracy
        self.tick_rate = 0.05
        self.abilities = paladin.abilities
        
        self.times_direct_healed = {}
        self.previous_ability = None
        
        self.access_token = access_token
        
        self.time_since_last_check = 0
        self.previous_total_healing = 0
        
        self.initial_state = copy.deepcopy(self)
                
    def simulate(self):
        while self.elapsed_time < self.encounter_length:
            if self.paladin.currently_casting is not None:
                self.paladin.remaining_cast_time -= self.tick_rate
                if self.paladin.remaining_cast_time <= 0:
                    self.complete_cast(self.paladin, self.elapsed_time)
                    self.paladin.currently_casting = None
            
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
            
            self.time_since_last_check += self.tick_rate
            if self.time_since_last_check >= 1:
                self.check_buff_counts()
                self.check_healing()
                self.check_resources()
                
            self.elapsed_time += self.tick_rate
        
    def check_healing(self):
        total_healing = 0
        for spell in self.paladin.ability_breakdown:
            total_healing += self.paladin.ability_breakdown[spell]["total_healing"]
            
        healing_this_second = total_healing - self.previous_total_healing
        self.previous_total_healing = total_healing
            
        self.paladin.healing_timeline.update({round(self.elapsed_time): healing_this_second})
        
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
            ("Divine Toll", lambda: self.previous_ability == "Daybreak"),
            ("Blessing of the Seasons", lambda: True),
            ("Avenging Wrath", lambda: True),
            # ("Light's Hammer", lambda: True),
            ("Tyr's Deliverance", lambda: True),
            ("Divine Favor", lambda: True),
            ("Light of Dawn", lambda: self.paladin.holy_power == 5),
            ("Daybreak", lambda: self.elapsed_time >= 12),
            ("Holy Shock", lambda: True),
            
            # ("Word of Glory", lambda: True),
            ("Crusader Strike", lambda: True),
            
            
            ("Judgment", lambda: True),
            ("Holy Light", lambda: True),
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
            
            update_self_buff_data(self.paladin.self_buff_breakdown, buff_name, self.elapsed_time, "expired")
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
                            target.apply_buff_to_target(HolyReverberation(self.paladin), self.elapsed_time, caster=self.paladin)
                            longest_reverberation_duration = max(buff_instance.duration for buff_instance in target.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in target.target_active_buffs and target.target_active_buffs["Holy Reverberation"] else None
                            if "Holy Reverberation" in target.target_active_buffs:
                                if len(target.target_active_buffs["Holy Reverberation"]) > 0:
                                    self.paladin.buff_events.append(f"{format_time(self.elapsed_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
                        append_aura_removed_event(self.paladin.buff_events, buff_name, self.paladin, target, self.elapsed_time)
                        del target.target_active_buffs[buff_name]
                        
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
    
    def add_spell_icons(self):
        for spell_id, spell_name in self.get_spell_ids().items():
            if spell_id not in self.spell_icons:
                spell_icon_data = cache.cached_get_spell_icon_data(self.access_token, spell_id)
                try:
                    self.spell_icons[spell_id] = spell_icon_data["assets"][0]["value"]
                except:
                    print(f"Spell: {spell_name} not found")
    
    def get_spell_ids_from_module(self, module_name):
        spell_ids = {}
        for name, obj in inspect.getmembers(sys.modules[module_name]):
            if inspect.isclass(obj) and hasattr(obj, "SPELL_ID"):
                spell_id = getattr(obj, "SPELL_ID")
                spell_ids[spell_id] = name
        return spell_ids
    
    def get_spell_ids(self):
        modules = [
            "app.classes.spells_healing",
            "app.classes.spells_damage",
            "app.classes.spells_auras",
            "app.classes.spells_passives",
            "app.classes.auras_buffs",
            "app.classes.auras_debuffs"
        ]
        
        all_spell_ids = {}
        for module in modules:
            all_spell_ids.update(self.get_spell_ids_from_module(module))
        
        # add misc spells    
        all_spell_ids.update({53563: "BeaconOfLight"})
        all_spell_ids.update({414127: "OverflowingLight"})
        all_spell_ids.update({392902: "ResplendentLight"})
        all_spell_ids.update({403042: "CrusadersReprieve"})
        all_spell_ids.update({385414: "Afterimage"})
        
        return all_spell_ids
    
    def reset_simulation(self):
        current_state = copy.deepcopy(self.initial_state)
        self.__dict__.update(current_state.__dict__)
        
    def display_results(self):
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
        
        full_awakening_trigger_times_results = {}

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
                "Blessing of Summer": "Blessing of the Seasons",
                "Blessing of Autumn": "Blessing of the Seasons",
                "Blessing of Winter": "Blessing of the Seasons",
                "Blessing of Spring": "Blessing of the Seasons",
            }

        # time the function
        start_time = time.time()
        
        # complete all simulation iterations and process the data of each
        for i in range(self.iterations):
            # reset simulation states
            print(i)
            emit('iteration_update', {'iteration': i + 1}, broadcast=True, namespace='/')
            self.paladin.reset_state()
            self.reset_simulation()
            
            # only record some data on the last iteration
            if i == self.iterations - 1:
                self.paladin.last_iteration = True
        
            self.simulate()
            
            ability_breakdown = self.paladin.ability_breakdown
            self_buff_breakdown = self.paladin.self_buff_breakdown
            target_buff_breakdown = self.paladin.target_buff_breakdown
            glimmer_counts = self.paladin.glimmer_counts
            tyrs_counts = self.paladin.tyrs_counts
            awakening_counts = self.paladin.awakening_counts
            healing_timeline = self.paladin.healing_timeline
            mana_timeline = self.paladin.mana_timeline
            holy_power_timeline = self.paladin.holy_power_timeline
            
            # pp.pprint(self.paladin.events)           
            # pp.pprint(ability_breakdown)
            
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
            for spell in ["Holy Shock (Divine Toll)", "Holy Shock (Divine Resonance)", "Holy Shock (Rising Sunlight)" , "Glimmer of Light", 
                        "Glimmer of Light (Daybreak)", "Glimmer of Light (Rising Sunlight)", "Glimmer of Light (Divine Toll)", 
                        "Glimmer of Light (Glistening Radiance (Light of Dawn))", "Glimmer of Light (Glistening Radiance (Word of Glory))", "Resplendent Light",
                        "Greater Judgment", "Judgment of Light", "Crusader's Reprieve", "Afterimage", "Reclamation (Holy Shock)", "Reclamation (Crusader Strike)", 
                        "Divine Revelations (Holy Light)", "Divine Revelations (Judgment)", "Blessing of Summer", "Blessing of Autumn",
                        "Blessing of Winter", "Blessing of Spring"]:
                if spell in ability_breakdown:
                    del ability_breakdown[spell]
                          
            # combine beacon glimmer sources into one spell
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
        
        all_ability_breakdown_iteration_results = get_all_iterations_results(full_ability_breakdown_results)
        combined_ability_breakdown_results = combine_results(*all_ability_breakdown_iteration_results)
        
        all_self_buff_breakdown_iteration_results = get_all_iterations_results(full_self_buff_breakdown_results)
        combined_self_buff_breakdown_results = combine_results(*all_self_buff_breakdown_iteration_results)
        
        all_target_buff_breakdown_iteration_results = get_all_iterations_results(full_target_buff_breakdown_results)
        combined_target_buff_breakdown_results = combine_results(*all_target_buff_breakdown_iteration_results)
        
        all_aggregated_target_buff_breakdown_iteration_results = get_all_iterations_results(full_aggregated_target_buff_breakdown_results)
        combined_aggregated_target_buff_breakdown_results = combine_results(*all_aggregated_target_buff_breakdown_iteration_results)
        
        all_glimmer_count_iteration_results = get_all_iterations_results(full_glimmer_count_results)
        combined_glimmer_count_results = combine_results(*all_glimmer_count_iteration_results)
        
        all_tyrs_count_iteration_results = get_all_iterations_results(full_tyrs_count_results)
        combined_tyrs_count_results = combine_results(*all_tyrs_count_iteration_results)
        
        all_awakening_count_iteration_results = get_all_iterations_results(full_awakening_count_results)
        combined_awakening_count_results = combine_results(*all_awakening_count_iteration_results)
        
        all_healing_timeline_iteration_results = get_all_iterations_results(full_healing_timeline_results)
        combined_healing_timeline_results = combine_results(*all_healing_timeline_iteration_results)
        
        all_mana_timeline_iteration_results = get_all_iterations_results(full_mana_timeline_results)
        combined_mana_timeline_results = combine_results(*all_mana_timeline_iteration_results)
        
        all_holy_power_timeline_iteration_results = get_all_iterations_results(full_holy_power_timeline_results)
        combined_holy_power_timeline_results = combine_results(*all_holy_power_timeline_iteration_results)
        
        average_ability_breakdown = average_out_simulation_results(combined_ability_breakdown_results, self.iterations)
        average_self_buff_breakdown = average_out_simulation_results(combined_self_buff_breakdown_results, self.iterations)
        average_target_buff_breakdown = average_out_simulation_results(combined_target_buff_breakdown_results, self.iterations)
        average_aggregated_target_buff_breakdown = average_out_simulation_results(combined_aggregated_target_buff_breakdown_results, self.iterations)
        average_glimmer_counts = average_out_simulation_results(combined_glimmer_count_results, self.iterations)
        average_tyrs_counts = average_out_simulation_results(combined_tyrs_count_results, self.iterations)
        average_awakening_counts = average_out_simulation_results(combined_awakening_count_results, self.iterations)
        average_healing_timeline = average_out_simulation_results(combined_healing_timeline_results, self.iterations)
        average_mana_timeline = average_out_simulation_results(combined_mana_timeline_results, self.iterations)
        average_holy_power_timeline = average_out_simulation_results(combined_holy_power_timeline_results, self.iterations)
        
        # healing_and_buff_events = sorted(self.paladin.events + self.paladin.buff_events, key=get_timestamp)
        # healing_and_beacon_events = sorted(self.paladin.events + self.paladin.beacon_events, key=get_timestamp)
        
        # print(f"Mana remaining: {self.paladin.mana}")

        # pp.pprint(healing_and_buff_events)
        # pp.pprint(healing_and_beacon_events)

        # pp.pprint(self.paladin.ability_cast_events)
        
        # this works for a 30s window
        # pp.pprint(self.paladin.holy_power_by_ability)
        # print(f"Glimmers applied: {self.paladin.glimmer_application_counter}")
        # print(f"Glimmers removed: {self.paladin.glimmer_removal_counter}")
        
        
        # pp.pprint(self.paladin.target_buff_breakdown)
        # pp.pprint(average_target_buff_breakdown)
        # pp.pprint(average_aggregated_target_buff_breakdown)
        
        # pp.pprint(average_awakening_counts)
        # pp.pprint(average_ability_breakdown)
        pp.pprint(self.paladin.events)
        
        full_results = {
            "healing_timeline": average_healing_timeline,
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
            "priority_breakdown": self.paladin.priority_breakdown
        }
        
        simulation_details = {
            "encounter_length": self.encounter_length,
            "paladin_name": self.paladin.name,
            "iterations": self.iterations,
            "max_mana": self.paladin.max_mana
        }
    
        end_time = time.time()
        simulation_time = end_time - start_time
        print(f"Simulation time: {simulation_time} seconds")

        # average_ability_breakdown, self.elapsed_time, None, average_self_buff_breakdown, average_target_buff_breakdown, 
        # average_aggregated_target_buff_breakdown, self.paladin.name, average_glimmer_counts, 
        # average_tyrs_counts, average_awakening_counts, average_healing_timeline, average_mana_timeline, full_awakening_trigger_times_results, average_holy_power_timeline
        return {"results": full_results, "simulation_details": simulation_details}
        
