import random

from ..utils.beacon_transfer_rates import beacon_transfer_rates_double_beacon
from ..utils.misc_functions import format_time, append_spell_heal_event, append_spell_beacon_event, calculate_beacon_healing, append_spell_started_casting_event, append_spell_cast_event, append_spell_damage_event, update_spell_data_heals, update_spell_data_casts, update_spell_data_beacon_heals, update_self_buff_data, update_target_buff_data, update_priority_breakdown
from collections import defaultdict

class Spell:
    
    def __init__(self, name, mana_cost=0, base_mana_cost=0, holy_power_gain=0, holy_power_cost=0, cooldown=0, max_charges=1,
                 hasted_cooldown=False, healing_target_count=1, damage_target_count=1, is_heal=False, is_damage_spell=False,
                 is_absorb=False, off_gcd=False, base_cast_time=0, applies_buff_to_target=False, bonus_crit=0, bonus_crit_healing=0,
                 bonus_versatility=0, bonus_mastery=0):
        self.name = name
        self.mana_cost = mana_cost
        self.base_mana_cost = base_mana_cost
        self.holy_power_gain = holy_power_gain
        self.holy_power_cost = holy_power_cost
        self.cooldown = cooldown
        self.remaining_cooldown = 0
        self.hasted_cooldown = hasted_cooldown
        self.healing_target_count = healing_target_count
        self.damage_target_count = damage_target_count
        self.is_heal = is_heal
        self.is_damage_spell = is_damage_spell
        self.is_absorb = is_absorb
        self.off_gcd = off_gcd
        self.max_charges = max_charges
        self.current_charges = self.max_charges
        self.base_cast_time = base_cast_time
        self.applies_buff_to_target = applies_buff_to_target
        
        self.spell_healing_modifier = 1.0
        self.spell_damage_modifier = 1.0
        
        self.bonus_crit = bonus_crit
        self.bonus_crit_healing = bonus_crit_healing
        self.bonus_versatility = bonus_versatility
        self.bonus_mastery = bonus_mastery
        
        self.cast_time_modifier = 1.0
        self.mana_cost_modifier = 1.0
        
        self.original_cooldown = None
        
        self.aoe_cast_counter = 0
    
    def start_cast_time(self, caster, ability, current_time):
        caster.currently_casting = ability.name
        caster.remaining_cast_time = self.calculate_cast_time(caster)
        append_spell_started_casting_event(caster.events, caster, ability, current_time)
        
    def can_cast(self, caster, current_time=0):
        if not self.off_gcd and caster.global_cooldown > 0:
            return False
        if self.max_charges > 0:
            if self.remaining_cooldown > 0 and self.current_charges == 0:
                return False    
        if caster.mana < self.get_mana_cost(caster):
            return False
        if hasattr(self, "holy_power_cost") and caster.holy_power < self.holy_power_cost:
            return False       
        return True
    
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):
        if not self.can_cast(caster):         
            return False
        
        spell_crit = False
        
        self.try_trigger_rppm_effects(caster, targets, current_time)
        
        for target in targets:
            mana_cost = self.get_mana_cost(caster)
            damage_value, is_crit = self.calculate_damage(caster, self.bonus_crit, self.bonus_versatility)
            damage_value = round(damage_value)
            target.receive_damage(damage_value)
            
            if self.healing_target_count > 0:
                caster.mana -= mana_cost / self.healing_target_count
            else:
                caster.mana -= mana_cost
            update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, self.holy_power_gain, self.holy_power_cost)
            
            update_spell_data_heals(caster.ability_breakdown, self.name, target, 0, is_crit)
            
            append_spell_damage_event(caster.events, self.name, caster, target, damage_value, current_time, is_crit, spends_mana=True)     
            append_spell_cast_event(caster.ability_cast_events, self.name, caster, current_time, target)    
        
        if self.current_charges == self.max_charges:    
            self.start_cooldown(caster)
            self.current_charges -= 1
        elif self.max_charges > 0:     
            self.current_charges -= 1
        
        caster.total_casts[self.name] = caster.total_casts.get(self.name, 0) + 1
        caster.cast_sequence.append(f"{self.name}: {current_time}")

        # update haste and gcd
        if not self.off_gcd:
            caster.global_cooldown = caster.hasted_global_cooldown

        return True, spell_crit
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        if not self.can_cast(caster):         
            return False
        
        spell_crit = False
        heal_amount = 0
        
        self.try_trigger_rppm_effects(caster, targets, current_time)
        
        # add auras to dictionaries and check current spell cooldownsfor display in priority list example
        self_auras = defaultdict(dict)
        for aura in caster.active_auras.values():
            self_auras[aura.name] = {"duration": caster.active_auras[aura.name].duration, "stacks": caster.active_auras[aura.name].current_stacks, "applied_duration": caster.active_auras[aura.name].base_duration}
            
        target_auras = defaultdict(dict)
        # for target in targets:
        #     for auras in target.target_active_buffs.values():
        #         for aura in auras:
        #             target_auras[target.name][aura.name] = {"duration": aura.duration, "stacks": aura.current_stacks, "applied_duration": aura.applied_duration}
        if self.healing_target_count == 1:
            for target in targets:
                for auras in target.target_active_buffs.values():
                    for aura in auras:
                        target_auras[target.name][aura.name] = {"duration": aura.duration, "stacks": aura.current_stacks, "applied_duration": aura.applied_duration}
        
        # count the auras active across all targets
        total_target_aura_counts = defaultdict(dict)
        for target in caster.potential_healing_targets:
            for aura in target.target_active_buffs:
                total_target_aura_counts[aura] = total_target_aura_counts.get(aura, 0) + 1
        
        # check cooldowns and add to priority breakdown
        spell_cooldowns = caster.check_cooldowns()
        
        # add spells that trigger other spells as a cast event and don't cost mana
        if self.name in ["Daybreak"]:
            update_spell_data_casts(caster.ability_breakdown, self.name, self.get_mana_cost(caster), self.holy_power_gain, self.holy_power_cost)
            update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts)
            
        # add spells that cost mana and don't heal
        if caster.mana >= self.get_mana_cost(caster) and self.get_mana_cost(caster) > 0 and not is_heal: 
            update_spell_data_casts(caster.ability_breakdown, self.name, self.get_mana_cost(caster), self.holy_power_gain, self.holy_power_cost)   
            update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, target_active_auras=target_auras, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts)
            
        # add spells that cost mana and do heal       
        elif caster.mana >= self.get_mana_cost(caster) and is_heal:  
            target_count = self.healing_target_count
            if target_count > 1:  
                multi_target_healing = [f"{self.name}: ", []]            
            for target in targets:            
                ability_healing = 0
                healing_value, is_crit = self.calculate_heal(caster, self.bonus_crit, self.bonus_versatility, self.bonus_mastery)
                
                mana_cost = self.get_mana_cost(caster)
                healing_value = round(healing_value)    
                target.receive_heal(healing_value)
                if target_count > 1:
                    # deduct mana on the first instance of a multi-target spell
                    if self.aoe_cast_counter == 0:
                        self.aoe_cast_counter = target_count               
                    if self.aoe_cast_counter == target_count:
                        caster.mana -= mana_cost
                        # add spell, mana cost, holy power attributes, and increment casts
                        if self.name in ["Light's Hammer"]:
                            update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost, exclude_casts=True)
                        else:
                            update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost)
                        
                    self.aoe_cast_counter -= 1
                else: 
                    caster.mana -= mana_cost
                    
                    # exclude casts for certain spells
                    if self.name in ["Tyr's Deliverance"]:
                        update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost, exclude_casts=True)
                    else:
                        update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost)
                
                # for detailed logging     
                caster.healing_by_ability[self.name] = caster.healing_by_ability.get(self.name, 0) + healing_value
                if is_crit:
                    spell_crit = True
                    caster.ability_crits[self.name] = caster.ability_crits.get(self.name, 0) + 1
                    
                if target_count == 1:
                    caster.healing_sequence.append(f"{self.name}: {current_time}, {healing_value}, {is_crit}")
                else:
                    multi_target_healing[1].append([healing_value, target.name, is_crit])
                 
                if target_count > 1:  
                    for aoe_heal in multi_target_healing[1]:
                        ability_healing = aoe_heal[0]
                        heal_amount += aoe_heal[0]
                else:      
                    ability_healing = healing_value   
                    heal_amount += healing_value             
            
                # add the target, healing, crit status, and increment hits
                update_spell_data_heals(caster.ability_breakdown, self.name, target, ability_healing, is_crit)
                if self.name not in ["Tyr's Deliverance", "Light's Hammer"]:
                    update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, target_active_auras=target_auras, heal=heal_amount, is_crit=is_crit, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts)    
                
                append_spell_heal_event(caster.events, self.name, caster, target, ability_healing, current_time, is_crit, spends_mana=True)   
                append_spell_cast_event(caster.ability_cast_events, self.name, caster, current_time, target)    
                
                # handle beacon healing
                beacon_healing = calculate_beacon_healing(self.name, healing_value)
                for beacon_target in caster.beacon_targets:
                    if target != beacon_target:
                        beacon_target.receive_beacon_heal(beacon_healing)
                        caster.healing_by_ability["Beacon of Light"] = caster.healing_by_ability.get("Beacon of Light", 0) + beacon_healing    
                        
                        update_spell_data_beacon_heals(caster.ability_breakdown, beacon_target, beacon_healing, self.name)
                        
                        # append_spell_heal_event(caster.events, "beacon", caster, beacon_target, beacon_healing, current_time, False, spends_mana=False)   
                        append_spell_beacon_event(caster.beacon_events, self.name, caster, beacon_target, healing_value, beacon_healing, current_time)   
                   
            if self.healing_target_count > 1:
                caster.healing_sequence.append(multi_target_healing)   

        if self.current_charges == self.max_charges:
            self.start_cooldown(caster)
            self.current_charges -= 1
        elif self.max_charges > 0:     
            self.current_charges -= 1

        if not is_heal:
            append_spell_cast_event(caster.ability_cast_events, self.name, caster, current_time)    
            caster.mana -= self.get_mana_cost(caster)
            
        # update details
        caster.total_casts[self.name] = caster.total_casts.get(self.name, 0) + 1
        caster.cast_sequence.append(f"{self.name}: {current_time}")

        # update haste and gcd
        if not self.off_gcd:
            caster.global_cooldown = caster.hasted_global_cooldown

        return True, spell_crit, heal_amount
    
    def calculate_cast_time(self, caster):
        return (self.base_cast_time / caster.haste_multiplier) * self.cast_time_modifier
    
    def calculate_heal(self, caster, bonus_crit=0, bonus_crit_healing=0, bonus_versatility=0, bonus_mastery=0):
        spell_power = caster.get_effective_spell_power()
        
        crit_multiplier = 1
        is_crit = False
        crit_chance = caster.crit + (self.bonus_crit * 100)
        random_num = random.random() * 100
        if random_num <= crit_chance:
            crit_multiplier = 2 + (self.bonus_crit_healing / 100)
            is_crit = True
          
        mastery_multiplier = 1 + ((caster.mastery_multiplier + self.bonus_mastery) - 1) * caster.mastery_effectiveness
        versatility_multiplier = caster.versatility_multiplier + self.bonus_versatility
        
        # overrides
        # spell_power = 8351
        # versatility_multiplier = 1.1782
        # mastery_multiplier = 1.261
        # print(f"{self.name}, SP: {spell_power}, COEFF: {self.SPELL_POWER_COEFFICIENT}, caster multiplier: {caster.healing_multiplier}, vers: {versatility_multiplier}, crit: {crit_multiplier}, mastery: {mastery_multiplier}, spell modifier: {self.spell_healing_modifier}")
        return spell_power * self.SPELL_POWER_COEFFICIENT * caster.healing_multiplier * versatility_multiplier * crit_multiplier * mastery_multiplier * self.spell_healing_modifier, is_crit
    
    def calculate_damage(self, caster, bonus_crit=0, bonus_versatility=0):
        spell_power = caster.get_effective_spell_power()
        
        crit_multiplier = 1
        is_crit = False
        crit_chance = caster.crit + (bonus_crit * 100)
        random_num = random.random() * 100
        if random_num <= crit_chance:
            crit_multiplier = 2
            is_crit = True
            
        versatility_multiplier = caster.versatility_multiplier + bonus_versatility
        return spell_power * self.SPELL_POWER_COEFFICIENT * caster.damage_multiplier * versatility_multiplier * crit_multiplier * self.spell_damage_modifier, is_crit
    
    def get_mana_cost(self, caster):
        return self.mana_cost * caster.base_mana * self.mana_cost_modifier
    
    def get_base_mana_cost(self, caster):
        return self.base_mana_cost * caster.base_mana
    
    def start_cooldown(self, caster):
        self.remaining_cooldown = self.calculate_cooldown(caster)
        self.original_cooldown = self.remaining_cooldown
        
    def calculate_cooldown(self, caster):
        if self.hasted_cooldown:
            haste_multiplier = caster.haste_multiplier
            return self.cooldown / haste_multiplier
        else:
            return self.cooldown
        
    def reset_cooldown(self, caster, current_time):
        caster.events.append(f"{format_time(current_time)}: {self.name}'s cooldown was reset")
        if self.current_charges < self.max_charges:
            self.current_charges += 1
            if self.current_charges == self.max_charges:
                self.remaining_cooldown = 0
        else:
            self.remaining_cooldown = 0
            
    def apply_holy_reverberation(self, caster, target, current_time):
        from .auras_buffs import HolyReverberation
        
        new_buff = HolyReverberation(caster)
        if "Holy Reverberation" in target.target_active_buffs:
            if len(target.target_active_buffs["Holy Reverberation"]) >= 6:
                shortest_buff = min(target.target_active_buffs["Holy Reverberation"], key=lambda buff: buff.duration)
                target.target_active_buffs["Holy Reverberation"].remove(shortest_buff)
                update_target_buff_data(caster.target_buff_breakdown, "Holy Reverberation", current_time, "stacks_decremented", target.name, stacks=len(target.target_active_buffs["Holy Reverberation"]))
            target.target_active_buffs["Holy Reverberation"].append(new_buff)
            update_target_buff_data(caster.target_buff_breakdown, "Holy Reverberation", current_time, "stacks_incremented", target.name, stacks=len(target.target_active_buffs["Holy Reverberation"]))
        else:
            target.target_active_buffs["Holy Reverberation"] = [new_buff]
            update_target_buff_data(caster.target_buff_breakdown, new_buff.name, current_time, "applied", target.name, new_buff.duration, new_buff.current_stacks)

        longest_reverberation_duration = max(buff.duration for buff in target.target_active_buffs["Holy Reverberation"])
        caster.buff_events.append(f"{format_time(current_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
        
    def try_trigger_rppm_effects(self, caster, targets, current_time):
        from .spells_passives import TouchOfLight
        from .auras_buffs import SophicDevotion
        
        def try_proc_rppm_effect(effect, is_hasted=True, is_heal=False, is_self_buff=False):
            # print(f"{effect.name}, {is_heal}, {is_self_buff}")
            caster.time_since_last_rppm_proc[effect.name] = caster.time_since_last_rppm_proc.get(effect.name, 0)
            
            if is_hasted:
                effect_proc_chance = (effect.BASE_PPM * caster.haste_multiplier) / 60
                effect_average_proc_interval = 60 / (effect.BASE_PPM * caster.haste_multiplier)
            else:
                effect_proc_chance = effect.BASE_PPM / 60
                effect_average_proc_interval = 60 / effect.BASE_PPM
                
            if effect.name in caster.time_since_last_rppm_proc:
                effect_proc_chance *= max(1, 1 + ((caster.time_since_last_rppm_proc[effect.name] / effect_average_proc_interval) - 1.5) * 3)
                
            if random.random() < effect_proc_chance:           
                # print(caster.time_since_last_rppm_proc)
                caster.time_since_last_rppm_proc[effect.name] = 0
                
                target = targets[0]
                if is_heal:
                    effect_heal, is_crit = effect.calculate_heal(caster)
                    target.receive_heal(effect_heal)
                    
                    update_spell_data_heals(caster.ability_breakdown, effect.name, target, effect_heal, is_crit)
                    append_spell_heal_event(caster.events, effect.name, caster, target, effect_heal, current_time, is_crit)
                    
                if is_self_buff:
                    caster.apply_buff_to_self(effect, current_time)
        
        if caster.is_talent_active("Touch of Light"):        
            touch_of_light = TouchOfLight(caster)        
            try_proc_rppm_effect(touch_of_light, is_heal=True)
            
        if "Sophic Devotion" in caster.bonus_enchants:
            sophic_devotion = SophicDevotion()
            try_proc_rppm_effect(sophic_devotion, is_self_buff=True)
   
        
class Wait(Spell):
# waits until next gcd

    def __init__(self):
        super().__init__("Wait")