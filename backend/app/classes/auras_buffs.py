import random
import re

from .auras import Buff
from ..utils.misc_functions import format_time, update_mana_gained, update_self_buff_data, update_spell_data_heals, add_talent_healing_multipliers, update_target_buff_data, calculate_sqrt_ability_scaling, try_proc_rppm_effect
from ..utils.stat_values import update_stat_with_multiplicative_percentage


class HoT(Buff):
    
    def __init__(self, name, duration, base_duration, base_tick_interval, initial_haste_multiplier, current_stacks=1, max_stacks=1, hasted=True):
        super().__init__(name, duration, base_duration, current_stacks=current_stacks, max_stacks=max_stacks) 
        self.base_tick_interval = base_tick_interval 
        self.time_until_next_tick = base_tick_interval
        self.total_ticks = 0
        self.previous_haste_multiplier = initial_haste_multiplier
        self.previous_tick_time = 0
        self.hasted = hasted
        
    def add_stack(self, new_buff_instance):
        self.buff_instances.append(new_buff_instance)
        
    def process_tick(self, caster, target, current_time, buff_instances, is_partial_tick=False):
        if is_partial_tick and not self.hasted:
            return
        
        total_heal_value, is_crit = self.calculate_tick_healing(caster) 
        
        total_heal_value *= len(buff_instances)
        
        if is_crit:
            total_heal_value *= 2
        
        if is_partial_tick:
            total_heal_value *= (current_time - self.previous_tick_time) / (self.base_tick_interval / caster.haste_multiplier)

        target.receive_heal(total_heal_value, caster)
        caster.handle_beacon_healing(self.name, target, total_heal_value, current_time)
        
        self.trigger_on_periodic_heal_effect(caster, current_time, target)
        
        if is_crit and self.name == "Holy Reverberation":
            caster.events.append(f"{format_time(current_time)}: Holy Reverberation crit healed {target.name} for {round(total_heal_value)}")
        elif self.name == "Holy Reverberation":
            caster.events.append(f"{format_time(current_time)}: Holy Reverberation healed {target.name} for {round(total_heal_value)}")
            
        self.total_ticks += 1 if not is_partial_tick else self.time_until_next_tick / self.base_tick_interval
        
        update_spell_data_heals(caster.ability_breakdown, self.name, target, total_heal_value, is_crit)
        
        if self.name == "Dawnlight (HoT)":
            self.radiate_healing(caster, current_time, total_heal_value)
             
    def calculate_tick_healing(self, caster, can_crit=True):
        spell_power = caster.spell_power
        
        total_healing = spell_power * self.SPELL_POWER_COEFFICIENT * caster.healing_multiplier
        
        mastery_multiplier = 1 + (caster.mastery_multiplier - 1) * caster.mastery_effectiveness
        versatility_multiplier = caster.versatility_multiplier
        total_healing *= mastery_multiplier * versatility_multiplier

        if self.hasted:
            number_of_ticks = self.base_duration / (self.base_tick_interval / caster.haste_multiplier)
            if number_of_ticks > 1:
                total_healing *= caster.haste_multiplier
            healing_per_tick = total_healing / number_of_ticks
        else:
            number_of_ticks = self.base_duration / self.base_tick_interval
            healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        if can_crit:
            crit_chance = caster.crit
            random_num = random.random() * 100
            if random_num <= crit_chance:
                is_crit = True
            
        healing_per_tick = add_talent_healing_multipliers(healing_per_tick, caster)

        return healing_per_tick, is_crit
    
    def trigger_on_periodic_heal_effect(self, caster, current_time, target):
        from .auras_buffs import (
            GaleOfShadows, BlessingOfAnshe
        )
        
        if self.name in ["Eternal Flame (HoT)", "Dawnlight (HoT)", "Sun Sear (HoT)"]:
            if caster.is_trinket_equipped("Gale of Shadows"):
                if "Gale of Shadows" in caster.active_auras:
                    gale_of_shadows = caster.active_auras["Gale of Shadows"]
                    
                    if gale_of_shadows.current_stacks < gale_of_shadows.max_stacks:
                        gale_of_shadows.remove_effect(caster)
                        gale_of_shadows.current_stacks += 1
                        gale_of_shadows.apply_effect(caster)
                    
                    gale_of_shadows.duration = gale_of_shadows.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Gale of Shadows", current_time, "applied", gale_of_shadows.duration, gale_of_shadows.current_stacks)               
                else:
                    caster.apply_buff_to_self(GaleOfShadows(caster), current_time, stacks_to_apply=1, max_stacks=20)
        
        if caster.is_talent_active("Blessing of An'she") and (self.name in ["Eternal Flame", "Dawnlight", "Sun Sear"]):
            blessing_of_anshe = BlessingOfAnshe(caster)
            try_proc_rppm_effect(caster, target, current_time, blessing_of_anshe, is_hasted=False, is_self_buff=True)
            


class GiftOfTheNaaruBuff(HoT):
    
    def __init__(self, caster):
        super().__init__("Gift of the Naaru", 5, base_duration=5, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        self.time_until_next_tick = self.base_tick_interval
        
    def calculate_tick_healing(self, caster):
        total_healing = caster.max_health * 0.2
        
        number_of_ticks = self.base_duration / self.base_tick_interval
        healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        crit_chance = caster.crit
        random_num = random.random() * 100
        if random_num <= crit_chance:
            is_crit = True

        return healing_per_tick, is_crit
        
        
class HolyReverberation(HoT):
    
    SPELL_POWER_COEFFICIENT = 1.08 * 0.8
    
    def __init__(self, caster):
        super().__init__("Holy Reverberation", 8, base_duration=8, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, current_stacks=1, max_stacks=6) 
        self.time_until_next_tick = self.base_tick_interval / caster.haste_multiplier
        

# trinket hots
class BroodkeepersPromiseHoT(HoT):
    
    def __init__(self, caster):
        super().__init__("Broodkeeper's Promise", 10000, base_duration=10000, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*?(\d+,?\d+)", trinket_effect)]
        
        # vers
        self.trinket_first_value = trinket_values[0]
        # healing
        self.trinket_second_value = trinket_values[1]
        
        # within 15 yards
        # vers
        self.trinket_first_value_bonus = trinket_values[0] * 1.5
        # healing
        self.trinket_second_value_bonus = trinket_values[1] * 2.34
    
    def calculate_tick_healing(self, caster):      
        versatility_multiplier = caster.versatility_multiplier
        healing_per_tick = ((self.trinket_second_value_bonus * 0.7) + (self.trinket_second_value * 0.3)) * versatility_multiplier
            
        healing_per_tick = add_talent_healing_multipliers(healing_per_tick, caster)

        return healing_per_tick, False
        

class Dawnlight(HoT):
    
    # TODO verify 22.5% higher
    SPELL_POWER_COEFFICIENT = 3.6 * 1.225
    
    def __init__(self, caster, duration_to_apply=8):
        super().__init__("Dawnlight (HoT)", duration_to_apply, base_duration=duration_to_apply, base_tick_interval=1.5, initial_haste_multiplier=caster.haste_multiplier) 
        self.time_until_next_tick = self.base_tick_interval / caster.haste_multiplier
        
        if "Morning Star" in caster.active_auras:
            self.SPELL_POWER_COEFFICIENT *= 1 + (0.05 * caster.active_auras["Morning Star"].current_stacks)
        
    def radiate_healing(self, caster, current_time, heal_amount):
        target_count = caster.variable_target_counts["Dawnlight"]
        
        scaling_factor = calculate_sqrt_ability_scaling(target_count, 5) / target_count
        # scaling is not currently working
        scaling_factor = 1
        
        targets = random.sample(caster.potential_healing_targets, target_count)
        for target in targets:            
        
            radiation_healing = heal_amount * 0.08 * scaling_factor
            # print(radiation_healing)

            target.receive_heal(radiation_healing, caster)
            update_spell_data_heals(caster.ability_breakdown, "Dawnlight (AoE)", target, radiation_healing, False)
            
            caster.handle_beacon_healing("Dawnlight (AoE)", target, radiation_healing, current_time)
            
    def remove_effect(self, caster, current_time, target):
        if "Sun's Avatar" in target.target_active_buffs:
            del target.target_active_buffs["Sun's Avatar"]
            update_target_buff_data(caster.target_buff_breakdown, "Sun's Avatar", current_time, "expired", target.name)
        
 
class EternalFlameBuff(HoT):
    
    SPELL_POWER_COEFFICIENT = 0.912 * 1.1
    
    def __init__(self, caster, duration_to_apply):
        super().__init__("Eternal Flame (HoT)", duration_to_apply, base_duration=duration_to_apply, base_tick_interval=3, initial_haste_multiplier=caster.haste_multiplier) 
        self.time_until_next_tick = self.base_tick_interval / caster.haste_multiplier


class SunSear(HoT):
    
    # TODO verify 22.5% higher
    SPELL_POWER_COEFFICIENT = 0.54 * 1.225
    
    def __init__(self, caster):
        super().__init__("Sun Sear", 4, base_duration=4, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier) 
        self.time_until_next_tick = self.base_tick_interval / caster.haste_multiplier
        

class HolyBulwarkBuff(HoT):
    
    def __init__(self, caster):
        super().__init__("Holy Bulwark", 20, base_duration=20, base_tick_interval=2, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        self.time_until_next_tick = self.base_tick_interval
        
    def calculate_tick_healing(self, caster):      
        healing_per_tick = caster.max_health * 0.02

        return healing_per_tick, False
    
    
# self buffs   
class AuraMasteryBuff(Buff):
    
    def __init__(self):
        super().__init__("Aura Mastery", 8, base_duration=8)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    
class MercifulAuras(Buff):
    
    def __init__(self):
        super().__init__("Merciful Auras", 10000, base_duration=10000)
        self.timer = 0
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    def trigger_passive_heal(self, caster, current_time):
        from .spells_healing import MercifulAurasHeal
        
        target_count = 3
        healing_modifier = 1
        
        if "Aura Mastery" in caster.active_auras:
            target_count = 20
            healing_modifier = 1.2
        
        targets = random.sample(caster.potential_healing_targets, target_count)
        for target in targets:            
            merciful_auras_heal, merciful_auras_crit = MercifulAurasHeal(caster).calculate_heal(caster)
            merciful_auras_heal *= healing_modifier

            target.receive_heal(merciful_auras_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Merciful Auras", target, merciful_auras_heal, merciful_auras_crit)
            
            caster.handle_beacon_healing("Merciful Auras", target, merciful_auras_heal, current_time)


class SavedByTheLight(Buff):
    
    def __init__(self):
        super().__init__("Saved by the Light", 10000, base_duration=10000)
        self.timer = 65
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    def trigger_passive_heal(self, caster, current_time):
        from .spells_healing import SavedByTheLightHeal
        
        if caster.is_talent_active("Beacon of Virtue"):
            target_count = 4
        elif caster.is_talent_active("Beacon of Faith"):
            target_count = 2
        else:
            target_count = 1
        
        targets = random.sample(caster.potential_healing_targets, target_count)
        for target in targets:            
            saved_by_the_light_heal, saved_by_the_light_crit = SavedByTheLightHeal(caster).calculate_heal(caster)
            if saved_by_the_light_crit:
                saved_by_the_light_heal /= 2

            target.receive_heal(saved_by_the_light_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Saved by the Light", target, saved_by_the_light_heal, False)
            
            caster.handle_beacon_healing("Saved by the Light", target, saved_by_the_light_heal, current_time)


class AvengingWrathBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Avenging Wrath", 20, base_duration=20)
        if caster.is_talent_active("Sanctified Wrath"):
            self.duration = 25
            self.base_duration = 25
        
    def apply_effect(self, caster, current_time=None):
        if "Avenging Wrath (Awakening)" in caster.active_auras:
            caster.active_auras["Avenging Wrath (Awakening)"].remove_effect(caster, current_time)
            del caster.active_auras["Avenging Wrath (Awakening)"]   
            update_self_buff_data(caster.self_buff_breakdown, "Avenging Wrath (Awakening)", current_time, "expired")      
        
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.flat_crit += 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier *= 1.15
        caster.damage_multiplier *= 1.15
        
        if caster.is_talent_active("Sanctified Wrath"):
            caster.abilities["Holy Shock"].cooldown *= 0.5
            caster.abilities["Holy Shock"].remaining_cooldown *= 0.5
            
        if caster.is_talent_active("Sun's Avatar"):
            caster.apply_buff_to_self(SunsAvatarActive(caster), current_time)
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.flat_crit -= 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier /= 1.15
        caster.damage_multiplier /= 1.15
        
        if caster.is_talent_active("Sanctified Wrath"):
            caster.abilities["Holy Shock"].cooldown /= 0.5
            caster.abilities["Holy Shock"].remaining_cooldown /= 0.5
            
        if caster.is_talent_active("Sun's Avatar") and "Sun's Avatar Active" in caster.active_auras:
            del caster.active_auras["Sun's Avatar Active"]   
            update_self_buff_data(caster.self_buff_breakdown, "Sun's Avatar Active", current_time, "expired")   
            
        for target in caster.potential_healing_targets:
            if "Sun's Avatar" in target.target_active_buffs:
                del target.target_active_buffs["Sun's Avatar"]
                update_target_buff_data(caster.target_buff_breakdown, "Sun's Avatar", current_time, "expired", target)
       
       
class AvengingWrathAwakening(Buff):
     
    def __init__(self):
        super().__init__("Avenging Wrath (Awakening)", 12, base_duration=12)
        
    def apply_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.flat_crit += 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier *= 1.15
        caster.damage_multiplier *= 1.15
        
        # sun's avatar
        if caster.is_talent_active("Dawnlight") and caster.is_talent_active("Sun's Avatar"):
            caster.apply_buff_to_self(SunsAvatarActive(caster), current_time)
            
            dawnlight_targets = [target for target in caster.potential_healing_targets if "Dawnlight (HoT)" in target.target_active_buffs]        
            non_dawnlight_targets = [target for target in caster.potential_healing_targets if "Dawnlight (HoT)" not in target.target_active_buffs]
            dawnlights_to_apply = 1
            chosen_targets = random.sample(non_dawnlight_targets, dawnlights_to_apply)
            for target in chosen_targets:
                target.apply_buff_to_target(Dawnlight(caster, 10), current_time, caster=caster)
                target.apply_buff_to_target(SunsAvatar(caster), current_time, caster=caster)
                
                if caster.is_talent_active("Solar Grace"):
                    caster.apply_buff_to_self(SolarGrace(caster), current_time)
            
                if caster.is_talent_active("Gleaming Rays"):
                    caster.apply_buff_to_self(GleamingRays(caster), current_time, reapply=True)
                
                if "Morning Star" in caster.active_auras:
                    caster.active_auras["Morning Star"].current_stacks = 0
                    
        # blessing of the forge
        if caster.is_talent_active("Blessing of the Forge"):
            sacred_weapon_targets = random.sample(caster.potential_healing_targets, 2)
            for target in sacred_weapon_targets:
                target.apply_buff_to_target(SacredWeaponBuff(caster), current_time, caster=caster)  
            if "Sacred Weapon" in caster.active_auras:
                caster.apply_buff_to_self(SacredWeaponSelf(caster), current_time, reapply=True)     
            else:      
                caster.apply_buff_to_self(SacredWeaponSelf(caster), current_time)
            caster.apply_buff_to_self(BlessingOfTheForge(caster, 12), current_time)
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.flat_crit -= 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier /= 1.15
        caster.damage_multiplier /= 1.15
        
        if caster.is_talent_active("Sun's Avatar") and "Sun's Avatar Active" in caster.active_auras:
            del caster.active_auras["Sun's Avatar Active"]   
            update_self_buff_data(caster.self_buff_breakdown, "Sun's Avatar Active", current_time, "expired")  
        
        for target in caster.potential_healing_targets:
            if "Sun's Avatar" in target.target_active_buffs:
                del target.target_active_buffs["Sun's Avatar"]
                update_target_buff_data(caster.target_buff_breakdown, "Sun's Avatar", current_time, "expired", target)
        

class AvengingCrusaderBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Avenging Crusader", 12, base_duration=12)          
        if caster.is_talent_active("Sanctified Wrath"):
            self.duration = 18
            self.base_duration = 18
        else:
            self.duration = 15
            self.base_duration = 15
        
    def apply_effect(self, caster, current_time=None):
        if "Avenging Crusader (Awakening)" in caster.active_auras:
            caster.active_auras["Avenging Crusader (Awakening)"].remove_effect(caster, current_time)
            del caster.active_auras["Avenging Crusader (Awakening)"]   
            update_self_buff_data(caster.self_buff_breakdown, "Avenging Crusader (Awakening)", current_time, "expired")      
        
        if caster.is_talent_active("Sanctified Wrath"):
            caster.abilities["Holy Shock"].cooldown *= 0.5
            caster.abilities["Holy Shock"].remaining_cooldown *= 0.5
            
        if caster.is_talent_active("Sun's Avatar"):
            caster.apply_buff_to_self(SunsAvatarActive(caster), current_time)
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Sanctified Wrath"):
            caster.abilities["Holy Shock"].cooldown /= 0.5
            caster.abilities["Holy Shock"].remaining_cooldown /= 0.5
            
        if caster.is_talent_active("Sun's Avatar") and "Sun's Avatar Active" in caster.active_auras:
            del caster.active_auras["Sun's Avatar Active"]   
            update_self_buff_data(caster.self_buff_breakdown, "Sun's Avatar Active", current_time, "expired")  
            
        for target in caster.potential_healing_targets:
            if "Sun's Avatar" in target.target_active_buffs:
                del target.target_active_buffs["Sun's Avatar"]
                update_target_buff_data(caster.target_buff_breakdown, "Sun's Avatar", current_time, "expired", target)
      
      
class AvengingCrusaderAwakening(Buff):
     
    def __init__(self):
        super().__init__("Avenging Crusader (Awakening)", 8, base_duration=8)
        
    def apply_effect(self, caster, current_time=None):
        # sun's avatar
        if caster.is_talent_active("Dawnlight") and caster.is_talent_active("Sun's Avatar"):
            caster.apply_buff_to_self(SunsAvatarActive(caster), current_time)
            
            dawnlight_targets = [target for target in caster.potential_healing_targets if "Dawnlight (HoT)" in target.target_active_buffs]        
            non_dawnlight_targets = [target for target in caster.potential_healing_targets if "Dawnlight (HoT)" not in target.target_active_buffs]
            dawnlights_to_apply = 1
            chosen_targets = random.sample(non_dawnlight_targets, dawnlights_to_apply)
            for target in chosen_targets:
                target.apply_buff_to_target(Dawnlight(caster, 10), current_time, caster=caster)
                target.apply_buff_to_target(SunsAvatar(caster), current_time, caster=caster)
                
                if caster.is_talent_active("Solar Grace"):
                    caster.apply_buff_to_self(SolarGrace(caster), current_time)
            
                if caster.is_talent_active("Gleaming Rays"):
                    caster.apply_buff_to_self(GleamingRays(caster), current_time, reapply=True)
                
                if "Morning Star" in caster.active_auras:
                    caster.active_auras["Morning Star"].current_stacks = 0
                    
        # blessing of the forge
        if caster.is_talent_active("Blessing of the Forge"):
            sacred_weapon_targets = random.sample(caster.potential_healing_targets, 2)
            for target in sacred_weapon_targets:
                target.apply_buff_to_target(SacredWeaponBuff(caster), current_time, caster=caster)  
            if "Sacred Weapon" in caster.active_auras:
                caster.apply_buff_to_self(SacredWeaponSelf(caster), current_time, reapply=True)     
            else:      
                caster.apply_buff_to_self(SacredWeaponSelf(caster), current_time)
            caster.apply_buff_to_self(BlessingOfTheForge(caster, 12), current_time)
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Sun's Avatar") and "Sun's Avatar Active" in caster.active_auras:
            del caster.active_auras["Sun's Avatar Active"]   
            update_self_buff_data(caster.self_buff_breakdown, "Sun's Avatar Active", current_time, "expired")  
        
        for target in caster.potential_healing_targets:
            if "Sun's Avatar" in target.target_active_buffs:
                del target.target_active_buffs["Sun's Avatar"]
                update_target_buff_data(caster.target_buff_breakdown, "Sun's Avatar", current_time, "expired", target)
  

class BarrierOfFaithBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Barrier of Faith", 24, base_duration=24)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass

        
class DivineFavorBuff(Buff):
    
    def __init__(self):
        super().__init__("Divine Favor", 10000)
        
    def apply_effect(self, caster, current_time=None):
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].spell_healing_modifier *= 1.4
            caster.abilities["Holy Light"].cast_time_modifier *= 0.7
            caster.abilities["Holy Light"].mana_cost_modifier *= 0.5
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].spell_healing_modifier *= 1.4
            caster.abilities["Flash of Light"].cast_time_modifier *= 0.7
            caster.abilities["Flash of Light"].mana_cost_modifier *= 0.5
            
    def remove_effect(self, caster, current_time=None):
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].spell_healing_modifier /= 1.4
            caster.abilities["Holy Light"].cast_time_modifier /= 0.7
            caster.abilities["Holy Light"].mana_cost_modifier /= 0.5
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].spell_healing_modifier /= 1.4
            caster.abilities["Flash of Light"].cast_time_modifier /= 0.7
            caster.abilities["Flash of Light"].mana_cost_modifier /= 0.5
 

class HandOfDivinityBuff(Buff):
     
    def __init__(self):
        super().__init__("Hand of Divinity", 20, base_duration=20, current_stacks=2, max_stacks=2)
        
    def apply_effect(self, caster, current_time=None):
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].spell_healing_modifier *= 1.3
            caster.abilities["Holy Light"].base_cast_time = 0
            caster.abilities["Holy Light"].mana_cost_modifier *= 0.5
            
    def remove_effect(self, caster, current_time=None):
        from ..classes.spells_healing import HolyLight
        
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].spell_healing_modifier /= 1.3
            caster.abilities["Holy Light"].base_cast_time = HolyLight.BASE_CAST_TIME
            caster.abilities["Holy Light"].mana_cost_modifier /= 0.5
       
        
class InfusionOfLight(Buff):
    
    def __init__(self, caster):
        super().__init__("Infusion of Light", 15, base_duration=15)
        if caster.is_talent_active("Inflorescence of the Sunwell"):
            self.current_stacks = 2
            self.max_stacks = 2
        
    def apply_effect(self, caster, current_time=None):
        if "Flash of Light" in caster.abilities and caster.is_talent_active("Inflorescence of the Sunwell"):
            caster.abilities["Flash of Light"].mana_cost_modifier *= 0
        elif "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].mana_cost_modifier *= 0.3
        
    def remove_effect(self, caster, current_time=None):
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].mana_cost_modifier = 1
            if "Divine Favor" in caster.active_auras:
                caster.abilities["Flash of Light"].mana_cost_modifier *= 0.7
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].holy_power_gain = 1


class DivineResonance(Buff):
    
    def __init__(self):
        super().__init__("Divine Resonance", 15, base_duration=15)
        self.last_holy_shock_time = 0
        
    def apply_effect(self, caster, current_time=None):
        self.last_holy_shock_time = 0
    
    def increment_divine_resonance(self, caster, current_time, tick_rate):
        self.last_holy_shock_time += tick_rate
        if self.last_holy_shock_time >= 5 - tick_rate - 0.01:
            self.trigger_divine_resonance_holy_shock(caster, current_time)
            self.last_holy_shock_time = 0
    
    def trigger_divine_resonance_holy_shock(self, caster, current_time):
        from .spells_healing import DivineResonanceHolyShock
        
        glimmer_targets = [glimmer_target for glimmer_target in caster.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        non_glimmer_targets = [glimmer_target for glimmer_target in caster.potential_healing_targets if "Glimmer of Light" not in glimmer_target.target_active_buffs]
        non_glimmer_non_beacon_targets = [t for t in non_glimmer_targets if t not in caster.beacon_targets] 
        target = [random.choice(non_glimmer_non_beacon_targets)]
        # target = [random.choice([t for t in caster.potential_healing_targets if t.name == "target18"])]
        DivineResonanceHolyShock(caster).cast_healing_spell(caster, target, current_time, is_heal=True, glimmer_targets=glimmer_targets)
        
        
class EmpyreanLegacy(Buff):
    
    def __init__(self):
        super().__init__("Empyrean Legacy", 20, base_duration=20)
        
    def apply_effect(self, caster, current_time=None):
        caster.apply_buff_to_self(EmpyreanLegacyCooldown(), current_time)
    
    def remove_effect(self, caster, current_time=None):
        pass
    

class EmpyreanLegacyCooldown(Buff):
    
    def __init__(self):
        super().__init__("Empyrean Legacy Cooldown", 20, base_duration=20)
        
    def apply_effect(self, caster, current_time=None):
        pass
    
    def remove_effect(self, caster, current_time=None):
        pass


class RelentlessInquisitor(Buff):
    
    def __init__(self):
        super().__init__("Relentless Inquisitor", 12, base_duration=12, current_stacks=1, max_stacks=5)
        
    def apply_effect(self, caster, current_time=None):
        update_stat_with_multiplicative_percentage(caster, "haste", (pow(1.01, self.current_stacks) - 1) * 100, True)
    
    def remove_effect(self, caster, current_time=None):
        update_stat_with_multiplicative_percentage(caster, "haste", (pow(1.01, self.current_stacks) - 1) * 100, False)

            
class RisingSunlight(Buff):
    
    def __init__(self, caster):
        super().__init__("Rising Sunlight", 30, base_duration=30, current_stacks=2, max_stacks=4)
        

class UnendingLight(Buff):
    
    def __init__(self, holy_power_spent):
        super().__init__("Unending Light", 30, base_duration=30, current_stacks=holy_power_spent, max_stacks=9)
       
        
class FirstLight(Buff):
    
    # casting Daybreak increases haste by 25% for 6 seconds
    def __init__(self):
        super().__init__("First Light", 6, base_duration=6)
        
    def apply_effect(self, caster, current_time=None):
        update_stat_with_multiplicative_percentage(caster, "haste", 25, True)
    
    def remove_effect(self, caster, current_time=None):
        update_stat_with_multiplicative_percentage(caster, "haste", 25, False)
        
        
class AwakeningStacks(Buff):
    
    def __init__(self):
        super().__init__("Awakening", 60, base_duration=60, current_stacks=1, max_stacks=15)
       
        
class AwakeningTrigger(Buff):
    
    def __init__(self):
        super().__init__("Awakening Ready", 30, base_duration=30)
        
        
class TyrsDeliveranceSelfBuff(Buff):
    
    def __init__(self):
        super().__init__("Tyr's Deliverance (self)", 20, base_duration=20)
        self.last_tyr_tick_time = 0
        self.base_tick_interval = 1
        
    def apply_effect(self, caster, current_time=None):
        self.last_tyr_tick_time = 0
        caster.tyrs_deliverance_extended_by = 0
    
    def increment_tyrs_deliverance(self, caster, current_time, tick_rate):
        self.last_tyr_tick_time += tick_rate
        if self.last_tyr_tick_time >= self.base_tick_interval / caster.haste_multiplier:
            self.trigger_tyrs_deliverance_tick(caster, current_time)
            self.last_tyr_tick_time = 0
    
    def trigger_tyrs_deliverance_tick(self, caster, current_time):
        from .spells_auras import TyrsDeliveranceHeal
        
        non_tyrs_targets = [target for target in caster.potential_healing_targets if "Tyr's Deliverance (target)" not in target.target_active_buffs]
        if len(non_tyrs_targets) > 0:
            target = [random.choice(non_tyrs_targets)]
        else:
            target = [random.choice(caster.potential_healing_targets)]
        # target = [random.choice([t for t in caster.potential_healing_targets if t.name == "target18"])]
        TyrsDeliveranceHeal(caster).cast_healing_spell(caster, target, current_time, is_heal=True)
        
    def trigger_partial_tick(self, caster, current_time):
        from .spells_auras import TyrsDeliveranceHeal
        
        non_tyrs_targets = [target for target in caster.potential_healing_targets if "Tyr's Deliverance (target)" not in target.target_active_buffs]
        if len(non_tyrs_targets) == 0:
            target = [random.choice(caster.potential_healing_targets)]
        else:
            target = [random.choice(non_tyrs_targets)]
        # target = [random.choice([t for t in caster.potential_healing_targets if t.name == "target18"])]
        spell = TyrsDeliveranceHeal(caster)
        hasted_tick_interval = self.base_tick_interval / caster.haste_multiplier

        # with a low tick rate if it lines up perfectly it can try to divide by 0
        spell.spell_healing_modifier *= (hasted_tick_interval - (hasted_tick_interval - self.last_tyr_tick_time - 0.0001)) / hasted_tick_interval
        spell.cast_healing_spell(caster, target, current_time, is_heal=True)
        spell.spell_healing_modifier /= (hasted_tick_interval - (hasted_tick_interval - self.last_tyr_tick_time  - 0.0001)) / hasted_tick_interval
        
        
class DivinePurpose(Buff):
    
    def __init__(self):
        super().__init__("Divine Purpose", 12, base_duration=12)
        
        
class BlessingOfDawn(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Dawn", 20, base_duration=20, current_stacks=1, max_stacks=2)
        
        
class BlessingOfDusk(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Dusk", 10, base_duration=10)
      
        
class SophicDevotion(Buff):
    
    BASE_PPM = 1
    
    def __init__(self):
        super().__init__("Sophic Devotion", 15, base_duration=15)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(932)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(932)
        

class PowerOfTheSilverHand(Buff):
    
    BASE_PPM = 1
    
    def __init__(self):
        super().__init__("Power of the Silver Hand", 10, base_duration=10)
        
    def apply_effect(self, caster, current_time=None):
        caster.apply_buff_to_self(PowerOfTheSilverHandStoredHealing(), current_time)
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class PowerOfTheSilverHandStoredHealing(Buff):
    
    def __init__(self):
        super().__init__("Power of the Silver Hand Stored Healing", 10, base_duration=10)
        self.stored_healing = 0
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class UntemperedDedication(Buff):
    
    def __init__(self):
        super().__init__("Untempered Dedication", 15, base_duration=15, current_stacks=1, max_stacks=5)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    
class MaraadsDyingBreath(Buff):
    
    def __init__(self, stacks_to_apply):
        super().__init__("Maraad's Dying Breath", 10, base_duration=10, current_stacks=stacks_to_apply, max_stacks=5)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
        

class Veneration(Buff):
    
    def __init__(self):
        super().__init__("Veneration", 15, base_duration=15)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
 
 
# target buffs   
class BeaconOfLightBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Beacon of Light", 10000, base_duration=10000)
        if caster.is_talent_active("Beacon of Virtue"):
            self.duration = 8
            self.base_duration = 8
        
             
class GlimmerOfLightBuff(Buff):
    
    def __init__(self):
        super().__init__("Glimmer of Light", 30, base_duration=30)
    
    
class BlessingOfFreedomBuff(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Freedom", 8, base_duration=8)
        
        
class TyrsDeliveranceTargetBuff(Buff):
    
    def __init__(self):
        super().__init__("Tyr's Deliverance (target)", 12, base_duration=12)
        
        
class BlessingOfSummer(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Summer", 30, base_duration=30)
        
        
class BlessingOfAutumn(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Autumn", 30, base_duration=30)
        
        
class BlessingOfWinter(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Winter", 30, base_duration=30)
        self.last_winter_tick_time = 0
        
    def apply_effect(self, caster, current_time=None):
        self.last_winter_tick_time = 0
        self.mana_gained = 0
    
    def increment_blessing_of_winter(self, caster, current_time, tick_rate):       
        self.last_winter_tick_time += tick_rate
        if self.last_winter_tick_time >= 2.94:
            winter_mana_gain = caster.max_mana * 0.01
            caster.mana += winter_mana_gain
            update_mana_gained(caster.ability_breakdown, "Blessing of Winter", winter_mana_gain)
            self.mana_gained += caster.max_mana * 0.01
            
            self.last_winter_tick_time = 0
            
        if caster.active_auras["Blessing of Winter"].duration < 0.01:
            caster.events.append(f"{format_time(current_time)}: {caster.name} gained {round(self.mana_gained)} mana from Blessing of Winter")
    
    
class BlessingOfSpring(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Spring", 30, base_duration=30)
        
    def apply_effect(self, caster, current_time=None):
        caster.healing_multiplier *= 1.15
        
    def remove_effect(self, caster, current_time=None):
        caster.healing_multiplier /= 1.15
        

class EmbraceOfPaku(Buff):
    
    BASE_PPM = 1
    
    def __init__(self):
        super().__init__("Embrace of Pa'ku", 12, base_duration=12)
        
    def apply_effect(self, caster, current_time=None):
        caster.flat_crit += 4
        caster.update_stat("crit", 0)
        
    def remove_effect(self, caster, current_time=None):
        caster.flat_crit -= 4
        caster.update_stat("crit", 0)
        

class FirebloodBuff(Buff):
    
    # TODO add an option for removing debuffs
    def __init__(self):
        super().__init__("Fireblood", 8, base_duration=8)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(875)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(875)
        
        
class TimeWarp(Buff):
    
    def __init__(self):
        super().__init__("Time Warp", 40, base_duration=40)
        
    def apply_effect(self, caster, current_time=None):
        update_stat_with_multiplicative_percentage(caster, "haste", 30, True)
    
    def remove_effect(self, caster, current_time=None):
        update_stat_with_multiplicative_percentage(caster, "haste", 30, False)
        
        
## consumables
# potions
class ElementalPotionOfUltimatePowerBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Elemental Potion of Ultimate Power", 30, base_duration=30)
        if "Potion Absorption Inhibitor" in caster.active_auras:
            self.duration *= 1 + (0.5 * caster.active_auras["Potion Absorption Inhibitor"].current_stacks)
            self.base_duration *= 1 + (0.5 * caster.active_auras["Potion Absorption Inhibitor"].current_stacks)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(886)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(886)
        

# phials
class IcedPhialOfCorruptingRage(Buff):
    
    def __init__(self):
        super().__init__("Iced Phial of Corrupting Rage", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.apply_buff_to_self(CorruptingRage(), current_time)
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class CorruptingRage(Buff):
    
    def __init__(self):
        super().__init__("Corrupting Rage", 65, base_duration=65)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 1118)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -1118)


class PhialOfTepidVersatility(Buff):
    
    def __init__(self):
        super().__init__("Phial of Tepid Versatility", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 745)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -745)
        
        
def apply_elemental_chaos_aura(caster, current_time):
        elemental_chaos_auras = [
            ElementalChaosAir,
            ElementalChaosEarth, 
            ElementalChaosFire,
            ElementalChaosFrost
        ]
        
        existing_buff = None
        for aura in caster.active_auras.values():
            if isinstance(aura, tuple(elemental_chaos_auras)):
                existing_buff = aura
                break
            
        chosen_aura_class = random.choice(elemental_chaos_auras)
        # print(f"{chosen_aura_class} chosen, {current_time}")

        if existing_buff and isinstance(existing_buff, chosen_aura_class):
            existing_buff.reapply_self(caster, current_time)          
        else:
            chosen_aura = chosen_aura_class()
            # print("APPLYING ELEMENTAL CHAOS AURA")
            caster.apply_buff_to_self(chosen_aura, current_time)
        
              
class PhialOfElementalChaos(Buff):
    
    def __init__(self):
        super().__init__("Phial of Elemental Chaos", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        apply_elemental_chaos_aura(caster, 0)
        
    def remove_effect(self, caster, current_time=None):
        pass
        
        
class ElementalChaosAir(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Air", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 652)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -652)
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        
        
class ElementalChaosFire(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Fire", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 652)
        caster.crit_damage_modifier += 0.02
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("crit", -652)
        caster.crit_damage_modifier -= 0.02
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)


class ElementalChaosFrost(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Frost", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 652)
        caster.crit_healing_modifier += 0.02
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("versatility", -652)
        caster.crit_healing_modifier -= 0.02
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        

class ElementalChaosEarth(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Earth", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 652)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("mastery", -652)
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        

def apply_alchemical_chaos_aura(caster, current_time):
        alchemical_chaos_auras = [
            AlchemicalChaosAir,
            AlchemicalChaosEarth, 
            AlchemicalChaosFire,
            AlchemicalChaosFrost
        ]
        
        existing_buff = None
        for aura in caster.active_auras.values():
            if isinstance(aura, tuple(alchemical_chaos_auras)):
                existing_buff = aura
                break
            
        chosen_aura_class = random.choice(alchemical_chaos_auras)

        if existing_buff and isinstance(existing_buff, chosen_aura_class):
            existing_buff.reapply_self(caster, current_time)          
        else:
            chosen_aura = chosen_aura_class()
            caster.apply_buff_to_self(chosen_aura, current_time)
        
              
class FlaskOfAlchemicalChaos(Buff):
    
    def __init__(self):
        super().__init__("Flask of Alchemical Chaos", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        apply_alchemical_chaos_aura(caster, 0)
        
    def remove_effect(self, caster, current_time=None):
        pass
        
        
class AlchemicalChaosAir(Buff):
    
    def __init__(self):
        super().__init__("Alchemical Chaos: Air", 30, base_duration=30)
        self.chosen_stats = []
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 3470)
        self.chosen_stats = random.sample(["crit", "versatility", "mastery"], 2)
        for stat in self.chosen_stats:
            caster.update_stat(stat, -290)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -3470)
        apply_alchemical_chaos_aura(caster, current_time)
        for stat in self.chosen_stats:
            caster.update_stat(stat, 290)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        
        
class AlchemicalChaosFire(Buff):
    
    def __init__(self):
        super().__init__("Alchemical Chaos: Fire", 30, base_duration=30)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 3470)
        self.chosen_stats = random.sample(["haste", "versatility", "mastery"], 2)
        for stat in self.chosen_stats:
            caster.update_stat(stat, -290)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("crit", -3470)
        apply_alchemical_chaos_aura(caster, current_time)
        for stat in self.chosen_stats:
            caster.update_stat(stat, 290)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)


class AlchemicalChaosFrost(Buff):
    
    def __init__(self):
        super().__init__("Alchemical Chaos: Frost", 30, base_duration=30)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 3470)
        self.chosen_stats = random.sample(["crit", "haste", "mastery"], 2)
        for stat in self.chosen_stats:
            caster.update_stat(stat, -290)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("versatility", -3470)
        apply_alchemical_chaos_aura(caster, current_time)
        for stat in self.chosen_stats:
            caster.update_stat(stat, 290)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        

class AlchemicalChaosEarth(Buff):
    
    def __init__(self):
        super().__init__("Alchemical Chaos: Earth", 30, base_duration=30)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 3470)
        self.chosen_stats = random.sample(["crit", "versatility", "haste"], 2)
        for stat in self.chosen_stats:
            caster.update_stat(stat, -290)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("mastery", -3470)
        apply_alchemical_chaos_aura(caster, current_time)
        for stat in self.chosen_stats:
            caster.update_stat(stat, 290)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)


class FlaskOfTemperedSwiftness(Buff):
    
    def __init__(self):
        super().__init__("Flask of Tempered Swiftness", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 2825)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -2825)
            

class FlaskOfTemperedAggression(Buff):
    
    def __init__(self):
        super().__init__("Flask of Tempered Aggression", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 2825)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -2825)
            

class FlaskOfTemperedMastery(Buff):
    
    def __init__(self):
        super().__init__("Flask of Tempered Mastery", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 2825)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -2825)
            
    
class FlaskOfTemperedVersatility(Buff):
    
    def __init__(self):
        super().__init__("Flask of Tempered Versatility", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 2825)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -2825)


class FlaskOfSavingGraces(Buff):
    
    def __init__(self):
        super().__init__("Flask of Saving Graces", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class SavingGraces(Buff):
    
    def __init__(self):
        super().__init__("Saving Graces", 10, base_duration=10)
        
    def apply_effect(self, caster, current_time=None):
        caster.healing_multiplier *= 1.10
        
    def remove_effect(self, caster, current_time=None):
        caster.healing_multiplier /= 1.10


class TemperedPotionBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Tempered Potion", 30, base_duration=30)
        if "Potion Absorption Inhibitor" in caster.active_auras:
            self.duration *= 1 + (0.5 * caster.active_auras["Potion Absorption Inhibitor"].current_stacks)
            self.base_duration *= 1 + (0.5 * caster.active_auras["Potion Absorption Inhibitor"].current_stacks)
            
        self.tempered_buffs = ["Flask of Tempered Swiftness", "Flask of Tempered Aggression", "Flask of Tempered Mastery", "Flask of Tempered Versatility"]
        for buff in caster.active_auras:
            if buff.name in self.tempered_buffs:
                self.tempered_buffs.remove(buff.name)
        
    def apply_effect(self, caster, current_time=None):
        if "Flask of Tempered Swiftness" in self.tempered_buffs:
            caster.update_stat("haste", 2617)
        if "Flask of Tempered Aggression" in self.tempered_buffs:
            caster.update_stat("crit", 2617)
        if "Flask of Tempered Mastery" in self.tempered_buffs:
            caster.update_stat("mastery", 2617)
        if "Flask of Tempered Versatility" in self.tempered_buffs:
            caster.update_stat("versatility", 2617)
        
    def remove_effect(self, caster, current_time=None):
        if "Flask of Tempered Swiftness" in self.tempered_buffs:
            caster.update_stat("haste", -2617)
        if "Flask of Tempered Aggression" in self.tempered_buffs:
            caster.update_stat("crit", -2617)
        if "Flask of Tempered Mastery" in self.tempered_buffs:
            caster.update_stat("mastery", -2617)
        if "Flask of Tempered Versatility" in self.tempered_buffs:
            caster.update_stat("versatility", -2617)


class SlumberingSoulSerumBuff(Buff):
        
    def __init__(self, caster):
        super().__init__("Slumbering Soul Serum", 10, base_duration=10)
        
    def apply_effect(self, caster, current_time=None):
        slumbering_soul_serum_mana_gain = 375000
        if "Algari Alchemist Stone" in caster.trinkets:
            slumbering_soul_serum_mana_gain *= 1.4
        caster.mana += slumbering_soul_serum_mana_gain
        update_mana_gained(caster.ability_breakdown, self.name, slumbering_soul_serum_mana_gain)
        caster.is_occupied = True
        
    def remove_effect(self, caster, current_time=None):
        caster.is_occupied = False


# food
class GrandBanquetOfTheKaluakFood(Buff):
    
    def __init__(self):
        super().__init__("Grand Banquet of the Kalu'ak", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(75)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(75)


class TimelyDemiseFood(Buff):
    
    def __init__(self):
        super().__init__("Timely Demise", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 105)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -105)

        
class FiletOfFangsFood(Buff):
    
    def __init__(self):
        super().__init__("Filet of Fangs", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 105)

        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -105)
        
        
class SeamothSurpriseFood(Buff):
    
    def __init__(self):
        super().__init__("Seamoth Surprise", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 105)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -105)


class SaltBakedFishcakeFood(Buff):
    
    def __init__(self):
        super().__init__("Salt-Baked Fishcake", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 105)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -105)
        
        
class FeistyFishSticksFood(Buff):
    
    def __init__(self):
        super().__init__("Feisty Fish Sticks", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 67)
        caster.update_stat("haste", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -67)
        caster.update_stat("haste", -67)
        

class AromaticSeafoodPlatterFood(Buff):
    
    def __init__(self):
        super().__init__("Aromatic Seafood Platter", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 67)
        caster.update_stat("haste", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -67)
        caster.update_stat("haste", -67)


class SizzlingSeafoodMedleyFood(Buff):
    
    def __init__(self):
        super().__init__("Sizzling Seafood Medley", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 67)
        caster.update_stat("haste", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -67)
        caster.update_stat("haste", -67)
        
        
class RevengeServedColdFood(Buff):
    
    def __init__(self):
        super().__init__("Revenge, Served Cold", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 67)
        caster.update_stat("versatility", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -67)
        caster.update_stat("versatility", -67)
        
        
class ThousandboneTongueslicerFood(Buff):
    
    def __init__(self):
        super().__init__("Thousandbone Tongueslicer", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 67)
        caster.update_stat("crit", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -67)
        caster.update_stat("crit", -67)


class GreatCeruleanSeaFood(Buff):
    
    def __init__(self):
        super().__init__("Great Cerulean Sea", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 67)
        caster.update_stat("versatility", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -67)
        caster.update_stat("versatility", -67)
        

class FeastOfTheDivineDay(Buff):
    
    def __init__(self):
        super().__init__("Feast of the Divine Day", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(446)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(446)
        

class TheSushiSpecial(Buff):
    
    def __init__(self):
        super().__init__("The Sushi Special", 10000, base_duration=10000)
        self.highest_stat = None
        
    def apply_effect(self, caster, current_time=None):
        self.highest_stat = caster.find_highest_secondary_stat_rating()
        caster.update_stat(self.highest_stat, 469)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat(self.highest_stat, -469)
        

class SaltBakedSeafood(Buff):
    
    def __init__(self):
        super().__init__("Salt Baked Seafood", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 235)
        caster.update_stat("crit", 235)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -235)
        caster.update_stat("crit", -235)
        
        
class MarinatedTenderloins(Buff):
    
    def __init__(self):
        super().__init__("Marinated Tenderloins", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 235)
        caster.update_stat("versatility", 235)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -235)
        caster.update_stat("versatility", -235)
        

class ChippyTea(Buff):
    
    def __init__(self):
        super().__init__("Chippy Tea", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 235)
        caster.update_stat("haste", 235)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -235)
        caster.update_stat("haste", -235)
        

class DeepfinPatty(Buff):
    
    def __init__(self):
        super().__init__("Deepfin Patty", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 235)
        caster.update_stat("crit", 235)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -235)
        caster.update_stat("crit", -235)
        

class SweetAndSpicySoup(Buff):
    
    def __init__(self):
        super().__init__("Sweet and Spicy Soup", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 235)
        caster.update_stat("versatility", 235)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -235)
        caster.update_stat("versatility", -235)
        

class FishAndChips(Buff):
    
    def __init__(self):
        super().__init__("Fish and Chips", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 235)
        caster.update_stat("crit", 235)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -235)
        caster.update_stat("crit", -235)
        

class StuffedCavePeppers(Buff):
    
    def __init__(self):
        super().__init__("Stuffed Cave Peppers", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(223)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(223)
        
        
# weapon imbues
class BuzzingRune(Buff):
    
    def __init__(self):
        super().__init__("Buzzing Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 310)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -310)


class ChirpingRune(Buff):
    
    def __init__(self):
        super().__init__("Chirping Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
        

class HowlingRune(Buff):
    
    def __init__(self):
        super().__init__("Howling Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 310)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -310)
        

class HissingRune(Buff):
    
    def __init__(self):
        super().__init__("Hissing Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 310)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -310)
        

class AlgariManaOil(Buff):
    
    def __init__(self):
        super().__init__("Algari Mana Oil", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 272)
        caster.update_stat("crit", 272)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -272)
        caster.update_stat("crit", -272)
        

class OilOfBeledarsGrace(Buff):
    
    def __init__(self):
        super().__init__("Oil of Beledar's Grace", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
        
        
# augment runes
class DraconicAugmentRune(Buff):
    
    def __init__(self):
        super().__init__("Draconic Augment Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(87)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(87)
        

class CrystallizedAugmentRune(Buff):
    
    def __init__(self):
        super().__init__("Crystallized Augment Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(733)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(733)
        
        
# RAID BUFFS
class ArcaneIntellect(Buff):
    
    def __init__(self):
        super().__init__("Arcane Intellect", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power *= 1.03
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power /= 1.03
        
        
class MarkOfTheWild(Buff):
    
    def __init__(self):
        super().__init__("Mark of the Wild", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.flat_versatility += 3
        caster.update_stat("versatility", 0)
        
    def remove_effect(self, caster, current_time=None):
        caster.flat_versatility -= 3
        caster.update_stat("versatility", 0)
        

class CloseToHeart(Buff):
    
    def __init__(self):
        super().__init__("Close to Heart", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    
class RetributionAura(Buff):
    
    def __init__(self):
        super().__init__("Retribution Aura ", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class RetributionAuraTrigger(Buff):
    
    def __init__(self):
        super().__init__("Retribution Aura", 30, base_duration=30)
        
    def apply_effect(self, caster, current_time=None):
        caster.healing_multiplier *= 1.02
        
    def remove_effect(self, caster, current_time=None):
        caster.healing_multiplier /= 1.02
        

class Skyfury(Buff):
    
    def __init__(self):
        super().__init__("Skyfury", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.flat_mastery += 2
        caster.update_stat("mastery", 0)
    
    def remove_effect(self, caster, current_time=None):
        caster.flat_mastery -= 2
        caster.update_stat("mastery", 0)
        

class ManaSpringTotem(Buff):
    
    def __init__(self):
        super().__init__("Mana Spring Totem", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class ManaTideTotem(Buff):
    
    def __init__(self):
        super().__init__("Mana Tide Totem", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class SymbolOfHope(Buff):
    
    def __init__(self):
        super().__init__("Symbol of Hope", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
        
        
# EXTERNAL BUFFS
class SourceOfMagic(Buff):
    
    def __init__(self):
        super().__init__("Source of Magic", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class PowerInfusion(Buff):
    def __init__(self):
        super().__init__("Power Infusion", 15, base_duration=15)
        
    def apply_effect(self, caster, current_time=None):
        caster.flat_haste += 20
        caster.update_stat("haste", 0)
        caster.update_hasted_cooldowns_with_haste_changes()
    
    def remove_effect(self, caster, current_time=None):
        caster.flat_haste -= 20
        caster.update_stat("haste", 0)
        caster.update_hasted_cooldowns_with_haste_changes()
        
        
class Innervate(Buff):
    def __init__(self):
        super().__init__("Innervate", 8, base_duration=8)
        
    def apply_effect(self, caster, current_time=None):
        caster.innervate_active = True
    
    def remove_effect(self, caster, current_time=None):
        caster.innervate_active = False
        

# trinkets
class NeltharionsCallToChaos(Buff):
    
    BASE_PPM = 1
    
    def __init__(self, caster):
        super().__init__("Neltharion's Call to Chaos", 18, base_duration=18)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
  
  
class IncarnatesMarkOfFire(Buff):
    
    def __init__(self, caster):
        super().__init__("Incarnate's Mark of Fire", 10000, base_duration=10000)
        trinket_effect = caster.trinkets["Whispering Incarnate Icon"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # passive haste
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("haste", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -self.trinket_first_value)
        

class InspiredByFrostAndEarth(Buff):
    
    # TODO check split on secondary stats
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Inspired by Frost and Earth", 12, base_duration=12)
        trinket_effect = caster.trinkets["Whispering Incarnate Icon"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # vers & crit proc  
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("crit", self.trinket_second_value)
        caster.update_stat("versatility", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -self.trinket_second_value)
        caster.update_stat("versatility", -self.trinket_second_value)
        

class VoiceFromBeyond(Buff):
    
    BASE_PPM = 5
    
    def __init__(self, caster):
        super().__init__("Voice from Beyond", 10000, base_duration=10000, current_stacks=1, max_stacks=9)
        
    def apply_effect(self, caster, current_time=None):      
        if caster.active_auras[self.name].current_stacks == 9:
            caster.apply_buff_to_self(TheSilentStar(caster), current_time)
            
            del caster.active_auras[self.name]
            update_self_buff_data(caster.self_buff_breakdown, "Voice from Beyond", current_time, "expired")   
        
    def remove_effect(self, caster, current_time=None):
        pass
        

class TheSilentStar(Buff):
    
    def __init__(self, caster):
        super().__init__("The Silent Star", 8, base_duration=8)
        cloak_effects = caster.equipment["back"]["effects"][0]["description"]
        cloak_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", cloak_effects)]
        
        self.stolen_value = cloak_values[0]
        self.gain_value = cloak_values[1]
        
        self.highest_stat = caster.find_highest_secondary_stat_rating()
        
    def apply_effect(self, caster, current_time=None):        
        if self.highest_stat == "haste":
            caster.update_stat("haste", self.gain_value + 4 * self.stolen_value)
        elif self.highest_stat == "crit":
            caster.update_stat("crit", self.gain_value + 4 * self.stolen_value)
        elif self.highest_stat == "mastery":
            caster.update_stat("mastery", self.gain_value + 4 * self.stolen_value)
        elif self.highest_stat == "versatility":
            caster.update_stat("versatility", self.gain_value + 4 * self.stolen_value)
        
    def remove_effect(self, caster, current_time=None):
        if self.highest_stat == "haste":
            caster.update_stat("haste", -1 * (self.gain_value + 4 * self.stolen_value))
        elif self.highest_stat == "crit":
            caster.update_stat("crit", -1 * (self.gain_value + 4 * self.stolen_value))
        elif self.highest_stat == "mastery":
            caster.update_stat("mastery", -1 * (self.gain_value + 4 * self.stolen_value))
        elif self.highest_stat == "versatility":
            caster.update_stat("versatility", -1 * (self.gain_value + 4 * self.stolen_value))


class SpoilsOfNeltharusBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Spoils of Neltharus", 20, base_duration=20)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # plus intellect
        self.trinket_first_value = trinket_values[0]
        
        self.chosen_stat = ""
        
    def apply_effect(self, caster, current_time=None):        
        self.chosen_stat = random.choice(["haste", "crit", "mastery", "versatility"])
        caster.update_stat(self.chosen_stat, self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat(self.chosen_stat, -self.trinket_first_value)


class TimeBreachingTalonPlus(Buff):
    
    def __init__(self, caster):
        super().__init__("Time-Breaching Talon ", 20, base_duration=20)
        trinket_effect = caster.trinkets["Time-Breaching Talon"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # plus intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        caster.apply_buff_to_self(TimeBreachingTalonMinus(caster), current_time)
        

class TimeBreachingTalonMinus(Buff):
    
    def __init__(self, caster):
        super().__init__("Time-Breaching Talon  ", 20, base_duration=20)
        trinket_effect = caster.trinkets["Time-Breaching Talon"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # minus intellect
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(self.trinket_second_value)


class EmeraldCoachsWhistle(Buff):
    
    BASE_PPM = 1
    
    def __init__(self, caster):
        super().__init__("Emerald Coach's Whistle", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # mastery
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("mastery", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -self.trinket_first_value)


class OminousChromaticEssence(Buff):
    
    def __init__(self, caster):
        super().__init__("Ominous Chromatic Essence", 10000, base_duration=10000)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # base
        self.trinket_first_value = trinket_values[0]
        # bonus
        self.trinket_second_value = trinket_values[1]
        
        self.available_stats = ["haste", "crit", "mastery", "versatility"]
        option_value = caster.trinkets.get(self.name, {}).get("option")

        if not option_value:
            self.chosen_stat = "mastery"
        else:
            self.chosen_stat = option_value.lower()
        self.available_stats.remove(self.chosen_stat)
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat(self.chosen_stat, self.trinket_first_value)
        for stat in self.available_stats:
            caster.update_stat(stat, self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat(self.chosen_stat, -self.trinket_first_value)
        for stat in self.available_stats:
            caster.update_stat(stat, -self.trinket_second_value)


class ScreamingBlackDragonscale(Buff):
    
    BASE_PPM = 3
    
    def __init__(self, caster):
        super().__init__("Screaming Black Dragonscale", 15, base_duration=15)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # crit
        self.trinket_first_value = trinket_values[0]
        # leech 
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("crit", self.trinket_first_value)
        caster.update_stat("leech", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -self.trinket_first_value)
        caster.update_stat("leech", -self.trinket_second_value)
        
        
class RashoksMoltenHeart(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Rashok's Molten Heart", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # mana
        self.trinket_first_value = trinket_values[0]
        # healing
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):     
        caster.mana += self.trinket_first_value
        update_mana_gained(caster.ability_breakdown, "Rashok's Molten Heart", self.trinket_first_value)
        
        from .spells_passives import RashoksMoltenHeartHeal
        targets = random.sample(caster.potential_healing_targets, 10)
        
        rashok_heal, _ = RashoksMoltenHeartHeal(caster).calculate_heal(caster)
        rashok_heal = self.trinket_second_value * caster.versatility_multiplier
        
        for target in targets:
            target.receive_heal(rashok_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Rashok's Molten Heart", target, rashok_heal, False)
        
    def remove_effect(self, caster, current_time=None):
        pass


class MirrorOfFracturedTomorrowsBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Mirror of Fractured Tomorrows", 20, base_duration=20)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # flat healing
        self.trinket_first_value = trinket_values[0]
        # highest secondary stat rating
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):  
        from .spells_passives import RestorativeSands
        target = random.choice(caster.potential_healing_targets)
        restorative_sands_heal, restorative_sands_crit = RestorativeSands(caster).calculate_heal(caster)
        restorative_sands_heal = self.trinket_first_value * caster.versatility_multiplier
        if restorative_sands_crit:
            restorative_sands_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
        
        # average 4 heals
        for i in range(4):
            target.receive_heal(restorative_sands_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Restorative Sands", target, restorative_sands_heal, restorative_sands_crit)
        
        self.highest_stat = caster.find_highest_secondary_stat_rating()
        
        if self.highest_stat == "haste":
            caster.update_stat("haste", self.trinket_second_value)
        elif self.highest_stat == "crit":
            caster.update_stat("crit", self.trinket_second_value)
        elif self.highest_stat == "mastery":
            caster.update_stat("mastery", self.trinket_second_value)
        elif self.highest_stat == "versatility":
            caster.update_stat("versatility", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        if self.highest_stat == "haste":
            caster.update_stat("haste", -self.trinket_second_value)
        elif self.highest_stat == "crit":
            caster.update_stat("crit", -self.trinket_second_value)
        elif self.highest_stat == "mastery":
            caster.update_stat("mastery", -self.trinket_second_value)
        elif self.highest_stat == "versatility":
            caster.update_stat("versatility", -self.trinket_second_value)
        

class CoagulatedGenesaurBloodBuff(Buff):
    
    BASE_PPM = 1.66
    
    def __init__(self, caster):
        super().__init__("Coagulated Genesaur Blood", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # crit
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("crit", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -self.trinket_first_value)
        

class SeaStarBuff(Buff):
    
    BASE_PPM = 1.5
    
    def __init__(self, caster):
        super().__init__("Sea Star", 15, base_duration=15)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):     
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        
        
class SustainingAlchemistStoneBuff(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Sustaining Alchemist Stone", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        

class AlacritousAlchemistStoneBuff(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Alacritous Alchemist Stone", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        caster.abilities["Potion"].remaining_cooldown -= 10
        caster.abilities["Potion"].shared_cooldown_end_time -= 10
        caster.abilities["Aerated Mana Potion"].remaining_cooldown -= 10
        caster.abilities["Elemental Potion of Ultimate Power"].remaining_cooldown -= 10
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        

class AlgariAlchemistStoneBuff(Buff):
    
    BASE_PPM = 1
    
    def __init__(self, caster):
        super().__init__("Algari Alchemist Stone", 15, base_duration=15)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
            
            
class PipsEmeraldFriendshipBadge(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Pip's Emerald Friendship Badge", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class BestFriendsWithPipEmpowered(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Pip Empowered", 12, base_duration=12)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.diminish_rate = 1/12
        self.diminished_value = 0
        self.last_update_time = 0
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", self.trinket_second_value)
        self.diminished_value = self.trinket_second_value
        self.last_update_time = current_time
        
    def remove_effect(self, caster, current_time, replaced=False):
        if not replaced:
            caster.apply_buff_to_self(BestFriendsWithPip(caster), current_time)
        caster.update_stat("mastery", -self.diminished_value)
            
    def diminish_effect(self, caster, current_time):
        time_since_update = current_time - self.last_update_time
        if time_since_update >= 1:
            self.diminished_value -= self.trinket_second_value * self.diminish_rate
            caster.update_stat("mastery", -self.trinket_second_value * self.diminish_rate)
            self.last_update_time = current_time
        
        
class BestFriendsWithPip(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Pip", 10000, base_duration=10000)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("mastery", -self.trinket_first_value)
        
        
class BestFriendsWithAerwynEmpowered(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Aerwyn Empowered", 12, base_duration=12)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.diminish_rate = 1/12
        self.diminished_value = 0
        self.last_update_time = 0
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.trinket_second_value)
        self.diminished_value = self.trinket_second_value
        self.last_update_time = current_time
        
    def remove_effect(self, caster, current_time, replaced=False):
        if not replaced:
            caster.apply_buff_to_self(BestFriendsWithAerwyn(caster), current_time)
        caster.update_stat("crit", -self.diminished_value)
            
    def diminish_effect(self, caster, current_time):
        time_since_update = current_time - self.last_update_time
        if time_since_update >= 1:
            self.diminished_value -= self.trinket_second_value * self.diminish_rate
            caster.update_stat("crit", -self.trinket_second_value * self.diminish_rate)
            self.last_update_time = current_time
        

class BestFriendsWithAerwyn(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Aerwyn", 10000, base_duration=10000)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("crit", -self.trinket_first_value)
        
        
class BestFriendsWithUrctosEmpowered(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Urctos Empowered", 12, base_duration=12)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.diminish_rate = 1/12
        self.diminished_value = 0
        self.last_update_time = 0
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.trinket_second_value)
        self.diminished_value = self.trinket_second_value
        self.last_update_time = current_time
        
    def remove_effect(self, caster, current_time, replaced=False):
        if not replaced:
            caster.apply_buff_to_self(BestFriendsWithUrctos(caster), current_time)
        caster.update_stat("versatility", -self.diminished_value)
            
    def diminish_effect(self, caster, current_time):
        time_since_update = current_time - self.last_update_time
        if time_since_update >= 1:
            self.diminished_value -= self.trinket_second_value * self.diminish_rate
            caster.update_stat("versatility", -self.trinket_second_value * self.diminish_rate)
            self.last_update_time = current_time
        
        
class BestFriendsWithUrctos(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Urctos", 10000, base_duration=10000)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("versatility", -self.trinket_first_value)
        
        
class IdolOfTheDreamerStacks(Buff):
    
    BASE_PPM = 2.2
    
    def __init__(self, caster):
        super().__init__("Idol of the Dreamer", 10000, base_duration=10000, current_stacks=caster.gem_counts["Ysemerald"], max_stacks=18 - caster.gem_counts["Ysemerald"])
        trinket_effect = caster.trinkets["Idol of the Dreamer"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        self.ysemerald_count = caster.gem_counts["Ysemerald"]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        if caster.active_auras[self.name].current_stacks == self.max_stacks:
            del caster.active_auras[self.name]
            self.remove_effect(caster, current_time)
            update_self_buff_data(caster.self_buff_breakdown, "Idol of the Dreamer", current_time, "expired")  
        else:
            caster.update_stat("haste", self.trinket_first_value * self.ysemerald_count) 
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -self.trinket_first_value * self.max_stacks)
        caster.apply_buff_to_self(IdolOfTheDreamerEmpower(caster), current_time)
    
    
class IdolOfTheDreamerEmpower(Buff):
    
    def __init__(self, caster):
        super().__init__("Idol of the Dreamer Empowered", 15, base_duration=15)
        trinket_effect = caster.trinkets["Idol of the Dreamer"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.trinket_second_value / 4)
        caster.update_stat("crit", self.trinket_second_value / 4)
        caster.update_stat("mastery", self.trinket_second_value / 4)
        caster.update_stat("versatility", self.trinket_second_value / 4)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -self.trinket_second_value / 4)
        caster.update_stat("crit", -self.trinket_second_value / 4)
        caster.update_stat("mastery", -self.trinket_second_value / 4)
        caster.update_stat("versatility", -self.trinket_second_value / 4)
 

class IdolOfTheLifeBinderStacks(Buff):
    
    BASE_PPM = 2.2
    
    def __init__(self, caster):
        super().__init__("Idol of the Life-Binder", 10000, base_duration=10000, current_stacks=caster.gem_counts["Alexstraszite"], max_stacks=18 - caster.gem_counts["Alexstraszite"])
        trinket_effect = caster.trinkets["Idol of the Life-Binder"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        self.alexstraszite_count = caster.gem_counts["Alexstraszite"]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        if caster.active_auras[self.name].current_stacks == self.max_stacks:
            del caster.active_auras[self.name]
            self.remove_effect(caster, current_time)
            update_self_buff_data(caster.self_buff_breakdown, "Idol of the Lifebinder", current_time, "expired")   
        else:
            caster.update_stat("crit", self.trinket_first_value * self.alexstraszite_count)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("crit", -self.trinket_first_value * self.max_stacks)
        caster.apply_buff_to_self(IdolOfTheLifeBinderEmpower(caster), current_time)
    

class IdolOfTheLifeBinderEmpower(Buff):
    
    def __init__(self, caster):
        super().__init__("Idol of the Life-Binder Empowered", 15, base_duration=15)
        trinket_effect = caster.trinkets["Idol of the Life-Binder"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.trinket_second_value / 4)
        caster.update_stat("crit", self.trinket_second_value / 4)
        caster.update_stat("mastery", self.trinket_second_value / 4)
        caster.update_stat("versatility", self.trinket_second_value / 4)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -self.trinket_second_value / 4)
        caster.update_stat("crit", -self.trinket_second_value / 4)
        caster.update_stat("mastery", -self.trinket_second_value / 4)
        caster.update_stat("versatility", -self.trinket_second_value / 4)


class IdolOfTheEarthWarderStacks(Buff):
    
    BASE_PPM = 2.2
    
    def __init__(self, caster):
        super().__init__("Idol of the Earth-Warder", 10000, base_duration=10000, current_stacks=caster.gem_counts["Neltharite"], max_stacks=18 - caster.gem_counts["Neltharite"])
        trinket_effect = caster.trinkets["Idol of the Earth-Warder"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        self.neltharite_count = caster.gem_counts["Neltharite"]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        
        if caster.active_auras[self.name].current_stacks == self.max_stacks:
            del caster.active_auras[self.name]
            self.remove_effect(caster, current_time)
            update_self_buff_data(caster.self_buff_breakdown, "Idol of the Earth-Warder", current_time, "expired")   
        else:
            caster.update_stat("mastery", self.trinket_first_value * self.neltharite_count)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("mastery", -self.trinket_first_value * self.max_stacks)
        caster.apply_buff_to_self(IdolOfTheEarthWarderEmpower(caster), current_time)
    

class IdolOfTheEarthWarderEmpower(Buff):
    
    def __init__(self, caster):
        super().__init__("Idol of the Earth-Warder Empowered", 15, base_duration=15)
        trinket_effect = caster.trinkets["Idol of the Earth-Warder"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.trinket_second_value / 4)
        caster.update_stat("crit", self.trinket_second_value / 4)
        caster.update_stat("mastery", self.trinket_second_value / 4)
        caster.update_stat("versatility", self.trinket_second_value / 4)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -self.trinket_second_value / 4)
        caster.update_stat("crit", -self.trinket_second_value / 4)
        caster.update_stat("mastery", -self.trinket_second_value / 4)
        caster.update_stat("versatility", -self.trinket_second_value / 4)
        
        
class IdolOfTheSpellWeaverStacks(Buff):
    
    BASE_PPM = 2.2
    
    def __init__(self, caster):
        super().__init__("Idol of the Spell-Weaver", 10000, base_duration=10000, current_stacks=caster.gem_counts["Malygite"], max_stacks=18 - caster.gem_counts["Malygite"])
        trinket_effect = caster.trinkets["Idol of the Spell-Weaver"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        self.malygite_count = caster.gem_counts["Malygite"]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        if caster.active_auras[self.name].current_stacks == self.max_stacks:
            del caster.active_auras[self.name]
            self.remove_effect(caster, current_time)
            update_self_buff_data(caster.self_buff_breakdown, "Idol of the Spell-Weaver", current_time, "expired")   
        else:
            caster.update_stat("versatility", self.trinket_first_value * self.malygite_count)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("versatility", -self.trinket_first_value * self.max_stacks)
        caster.apply_buff_to_self(IdolOfTheSpellWeaverEmpower(caster), current_time)
    

class IdolOfTheSpellWeaverEmpower(Buff):
    
    def __init__(self, caster):
        super().__init__("Idol of the Spell-Weaver Empowered", 15, base_duration=15)
        trinket_effect = caster.trinkets["Idol of the Spell-Weaver"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.trinket_second_value / 4)
        caster.update_stat("crit", self.trinket_second_value / 4)
        caster.update_stat("mastery", self.trinket_second_value / 4)
        caster.update_stat("versatility", self.trinket_second_value / 4)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -self.trinket_second_value / 4)
        caster.update_stat("crit", -self.trinket_second_value / 4)
        caster.update_stat("mastery", -self.trinket_second_value / 4)
        caster.update_stat("versatility", -self.trinket_second_value / 4)
        

class EchoingTyrstoneBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Echoing Tyrstone", 15, base_duration=15)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -self.trinket_second_value)
        
        
class SmolderingSeedlingActive(Buff):
    
    def __init__(self, caster):
        super().__init__("Smoldering Seedling active", 12, base_duration=12)
        from .target import SmolderingSeedling
        
        trinket_effect = caster.trinkets["Smoldering Seedling"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.smoldering_seedling = SmolderingSeedling("smoldering_seedling", caster)
        
    def apply_effect(self, caster, current_time=None):
        if self.smoldering_seedling not in caster.potential_healing_targets:
            caster.potential_healing_targets.append(self.smoldering_seedling)
        
    def remove_effect(self, caster, current_time=None):
        if self.smoldering_seedling in caster.potential_healing_targets:
            caster.potential_healing_targets.remove(self.smoldering_seedling)
        caster.apply_buff_to_self(SmolderingSeedlingBuff(caster), current_time)
        

class SmolderingSeedlingBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Smoldering Seedling", 10, base_duration=10)      
        trinket_effect = caster.trinkets["Smoldering Seedling"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -self.trinket_second_value)
        

class BlossomOfAmirdrassilLargeHoT(HoT):
    
    def __init__(self, caster):
        super().__init__("Blossom of Amirdrassil Large HoT", 6, base_duration=6, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        self.time_until_next_tick = self.base_tick_interval
        trinket_effect = caster.trinkets["Blossom of Amirdrassil"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # initial HoT
        self.trinket_first_value = trinket_values[0]
        
    def calculate_tick_healing(self, caster):
        total_healing = self.trinket_first_value * caster.versatility_multiplier
        
        if "Blessing of Spring" in caster.active_auras:
            total_healing *= 1.15
            
        if "Close to Heart" in caster.active_auras:
            total_healing *= 1.04
            
        if "Aura Mastery" in caster.active_auras and caster.is_talent_active("Protection of Tyr"):
            total_healing *= 1.1
        
        number_of_ticks = self.base_duration / self.base_tick_interval
        healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        crit_chance = caster.crit
        random_num = random.random() * 100
        if random_num <= crit_chance:
            is_crit = True

        return healing_per_tick, is_crit


class BlossomOfAmirdrassilSmallHoT(HoT):
    
    def __init__(self, caster):
        super().__init__("Blossom of Amirdrassil Small HoT", 6, base_duration=6, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        self.time_until_next_tick = self.base_tick_interval
        trinket_effect = caster.trinkets["Blossom of Amirdrassil"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # three target HoT
        self.trinket_second_value = trinket_values[1]
        
    def calculate_tick_healing(self, caster):
        total_healing = self.trinket_second_value * caster.versatility_multiplier
        
        if "Blessing of Spring" in caster.active_auras:
            total_healing *= 1.15
            
        if "Close to Heart" in caster.active_auras:
            total_healing *= 1.04
            
        if "Aura Mastery" in caster.active_auras and caster.is_talent_active("Protection of Tyr"):
            total_healing *= 1.1
        
        number_of_ticks = self.base_duration / self.base_tick_interval
        healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        crit_chance = caster.crit
        random_num = random.random() * 100
        if random_num <= crit_chance:
            is_crit = True

        return healing_per_tick, is_crit
    

class NymuesUnravelingSpindleBuff(Buff):
    def __init__(self, caster):
        super().__init__("Nymue's Unraveling Spindle", 18, base_duration=18)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # mastery buff
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("mastery", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -self.trinket_first_value)
        

class HarvestersEdict(Buff):
    
    BASE_PPM = 1.66
    
    def __init__(self, caster):
        super().__init__("Harvester's Edict", 15, base_duration=15)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # mastery buff
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("mastery", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -self.trinket_first_value)
        

class AraKaraSacbrood(Buff):
    
    BASE_PPM = 2.5
    count = 0

    def __init__(self, caster):
        self.count = AraKaraSacbrood.count

        super().__init__(f"Ara-Kara Sacbrood", 60, base_duration=60)
        trinket_effect = caster.trinkets["Ara-Kara Sacbrood"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
            
        self.trinket_intellect_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):    
        caster.spell_power += caster.get_effective_spell_power(self.trinket_intellect_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_intellect_value)
        
        
class EmpoweringCrystalOfAnubikkaj(Buff):
    
    BASE_PPM = 1.55
    
    def __init__(self, caster):
        super().__init__("Empowering Crystal of Anub'ikkaj", 20, base_duration=20)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # random secondary stat buff
        self.trinket_first_value = trinket_values[0]
        self.chosen_stat = ""
        
    def apply_effect(self, caster, current_time=None):        
        self.chosen_stat = random.choice(["haste", "crit", "mastery", "versatility"])
        caster.update_stat(self.chosen_stat, self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat(self.chosen_stat, -self.trinket_first_value)
        

class UnboundChangeling(Buff):
    
    BASE_PPM = 1.5
    
    def __init__(self, caster):
        super().__init__("Unbound Changeling", 12, base_duration=12)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        
        self.available_stats = ["haste", "crit", "mastery", "combined"]
        option_value = caster.trinkets.get(self.name, {}).get("option")

        if not option_value:
            self.chosen_stat = "mastery"
        else:
            self.chosen_stat = option_value.lower()
        self.available_stats.remove(self.chosen_stat)
        
        if self.chosen_stat == "combined":
            self.trinket_first_value *= (1.2571 / 3)
        
    def apply_effect(self, caster, current_time=None):    
        if self.chosen_stat == "combined":
            caster.update_stat("haste", self.trinket_first_value)
            caster.update_stat("crit", self.trinket_first_value)
            caster.update_stat("mastery", self.trinket_first_value)
        else:
            caster.update_stat(self.chosen_stat, self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        if self.chosen_stat == "combined":
            caster.update_stat("haste", -self.trinket_first_value)
            caster.update_stat("crit", -self.trinket_first_value)
            caster.update_stat("mastery", -self.trinket_first_value)
        else:
            caster.update_stat(self.chosen_stat, -self.trinket_first_value)
        
        
class HighSpeakersAccretionRift(Buff):
    
    def __init__(self, caster):
        super().__init__("High Speaker's Accretion Rift", 6, base_duration=6)
        
    def apply_effect(self, caster, current_time=None):    
        pass
        
    def remove_effect(self, caster, current_time=None):
        caster.apply_buff_to_self(HighSpeakersAccretionIntellect(caster), current_time)
    

class HighSpeakersAccretionIntellect(Buff):
    
    def __init__(self, caster):
        super().__init__("High Speaker's Accretion Intellect", 20, base_duration=20)
        trinket_effect = caster.trinkets["High Speaker's Accretion"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        option_value = caster.trinkets.get("High Speaker's Accretion", {}).get("option")

        if not option_value:
            self.target_count = 1
        else:
            self.target_count = int(option_value)
            
        self.trinket_intellect_value = trinket_values[1] * self.target_count
        
    def apply_effect(self, caster, current_time=None):    
        caster.spell_power += caster.get_effective_spell_power(self.trinket_intellect_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_intellect_value)
        
        
class OvinaxsMercurialEggBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Ovinax's Mercurial Egg", 10000, base_duration=10000)
        self.moving = False
        self.timer = 0
        
    def apply_effect(self, caster, current_time=None):
        caster.apply_buff_to_self(DeliberateIncubation(caster, stacks_to_apply=30), 0)
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class OvinaxsMercurialEggPaused(Buff):
        
        def __init__(self, caster):
            super().__init__("Ovinax's Mercurial Egg Paused", 20, base_duration=20)
            
        def apply_effect(self, caster, current_time=None):
            pass
            
        def remove_effect(self, caster, current_time=None):
            pass
        
        
class DeliberateIncubation(Buff):
    
    def __init__(self, caster, stacks_to_apply=1):
        super().__init__("Deliberate Incubation", 10000, base_duration=10000, current_stacks=stacks_to_apply, max_stacks=30)
        trinket_effect = caster.trinkets["Ovinax's Mercurial Egg"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_intellect_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):
        if self.current_stacks > 20:  
            caster.spell_power += caster.get_effective_spell_power(self.trinket_intellect_value * 20 + (self.trinket_intellect_value * 0.6 * (self.current_stacks - 20)))
        else:
            caster.spell_power += caster.get_effective_spell_power(self.trinket_intellect_value * self.current_stacks)
        
    def remove_effect(self, caster, current_time=None):
        if self.current_stacks > 20:    
            caster.spell_power -= caster.get_effective_spell_power(self.trinket_intellect_value * 20 + (self.trinket_intellect_value * 0.6 * (self.current_stacks - 20)))
        else:
            caster.spell_power -= caster.get_effective_spell_power(self.trinket_intellect_value * self.current_stacks)
        

class RecklessIncubation(Buff):
    
    def __init__(self, caster):
        super().__init__("Reckless Incubation", 10000, base_duration=10000, current_stacks=1, max_stacks=30)
        trinket_effect = caster.trinkets["Ovinax's Mercurial Egg"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_secondary_stat_value = trinket_values[1]
        self.highest_stat = caster.find_highest_secondary_stat_rating()
        
    def apply_effect(self, caster, current_time=None):    
        if self.current_stacks > 20:  
            caster.update_stat(self.highest_stat, self.trinket_secondary_stat_value * 20 + (self.trinket_secondary_stat_value * 0.6 * (self.current_stacks - 20)))
        else:
            caster.update_stat(self.highest_stat, self.trinket_secondary_stat_value * self.current_stacks)
        
    def remove_effect(self, caster, current_time=None):
        if self.current_stacks > 20:    
            caster.update_stat(self.highest_stat, -self.trinket_secondary_stat_value * 20 + (-self.trinket_secondary_stat_value * 0.6 * (self.current_stacks - 20)))
        else:
            caster.update_stat(self.highest_stat, -self.trinket_secondary_stat_value * self.current_stacks)
        

# Treacherous Transmitter RNG proc removed for now
# class CrypticInstructions(Buff):
    
#     BASE_PPM = 6
    
#     def __init__(self, caster):
#         super().__init__("Cryptic Instructions", 10000, base_duration=10000, current_stacks=1, max_stacks=10)
        
#     def apply_effect(self, caster, current_time=None):    
#         if caster.active_auras[self.name].current_stacks == self.max_stacks:
#             del caster.active_auras[self.name]
#             self.remove_effect(caster, current_time)
#             update_self_buff_data(caster.self_buff_breakdown, "Cryptic Instructions", current_time, "expired")  
        
#     def remove_effect(self, caster, current_time=None):
#         caster.apply_buff_to_self(EtherealPowerlink(caster), current_time)
    

class EtherealPowerlink(Buff):
    
    def __init__(self, caster, stacks_to_apply=1):
        super().__init__("Ethereal Powerlink", 15, base_duration=15)
        trinket_effect = caster.trinkets["Treacherous Transmitter"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):    
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        

class FateweavedNeedle(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Fateweaved Needle", 5, base_duration=5)
        weapon_effects = caster.equipment["main_hand"]["effects"][0]["description"]
        weapon_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", weapon_effects)]
        
        # intellect
        self.effect_first_value = weapon_values[0]
        
    def apply_effect(self, caster, current_time=None):    
        caster.spell_power += caster.get_effective_spell_power(self.effect_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.effect_first_value)
        
        
class VolatileSerum(Buff):
    
    BASE_PPM = 6
    
    def __init__(self, caster):
        super().__init__("Volatile Serum", 15, base_duration=15)
        
    def apply_effect(self, caster, current_time=None):    
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass


class ImperfectAscendancySerumBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Imperfect Ascendancy Serum", 20, base_duration=20)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        # secondaries
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):    
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        caster.update_stat("haste", self.trinket_second_value)
        caster.update_stat("crit", self.trinket_second_value)
        caster.update_stat("mastery", self.trinket_second_value)
        caster.update_stat("versatility", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        caster.update_stat("haste", -self.trinket_second_value)
        caster.update_stat("crit", -self.trinket_second_value)
        caster.update_stat("mastery", -self.trinket_second_value)
        caster.update_stat("versatility", -self.trinket_second_value)


# embellishments
class PotionAbsorptionInhibitor(Buff):
    
    def __init__(self, caster):
        super().__init__("Potion Absorption Inhibitor", 10000, base_duration=10000)   
        if caster.embellishments["Potion Absorption Inhibitor"]["count"] == 2:
            self.current_stacks = 2
            self.max_stacks = 2
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    
class ElementalLariat(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Elemental Lariat", 5 + caster.total_elemental_gems, base_duration=5 + caster.total_elemental_gems)   
        embellishment_effect = caster.embellishments[self.name]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        
        self.air_gems_count = caster.gem_types["Air"]
        self.fire_gems_count = caster.gem_types["Fire"]
        self.earth_gems_count = caster.gem_types["Earth"]
        self.frost_gems_count = caster.gem_types["Frost"]
        
        self.chosen_stat = ""
        
    def apply_effect(self, caster, current_time=None):
        choices = self.air_gems_count * ["haste"] + self.fire_gems_count * ["crit"] + self.earth_gems_count * ["mastery"] + self.frost_gems_count * ["versatility"]
        self.chosen_stat = random.choice(choices)
        
        if self.chosen_stat == "haste":
            caster.apply_buff_to_self(ElementalLariatHaste(caster), current_time)
        elif self.chosen_stat == "crit":
            caster.apply_buff_to_self(ElementalLariatCrit(caster), current_time)
        elif self.chosen_stat == "mastery":
            caster.apply_buff_to_self(ElementalLariatMastery(caster), current_time)
        elif self.chosen_stat == "versatility":
            caster.apply_buff_to_self(ElementalLariatVersatility(caster), current_time)
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class ElementalLariatHaste(Buff):
    
    def __init__(self, caster):
        super().__init__("Elemental Lariat - Haste", 5 + caster.total_elemental_gems, base_duration=5 + caster.total_elemental_gems)   
        embellishment_effect = caster.embellishments["Elemental Lariat"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
      
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -self.embellishment_first_value)
        
        
class ElementalLariatCrit(Buff):
    
    def __init__(self, caster):
        super().__init__("Elemental Lariat - Crit", 5 + caster.total_elemental_gems, base_duration=5 + caster.total_elemental_gems)   
        embellishment_effect = caster.embellishments["Elemental Lariat"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -self.embellishment_first_value)
        

class ElementalLariatMastery(Buff):
    
    def __init__(self, caster):
        super().__init__("Elemental Lariat - Mastery", 5 + caster.total_elemental_gems, base_duration=5 + caster.total_elemental_gems)   
        embellishment_effect = caster.embellishments["Elemental Lariat"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -self.embellishment_first_value)
        
        
class ElementalLariatVersatility(Buff):
    
    def __init__(self, caster):
        super().__init__("Elemental Lariat - Versatility", 5 + caster.total_elemental_gems, base_duration=5 + caster.total_elemental_gems)   
        embellishment_effect = caster.embellishments["Elemental Lariat"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -self.embellishment_first_value)
    
    
class AlliedChestplateOfGenerosity(Buff):
    
    BASE_PPM = 1
    
    def __init__(self, caster):
        super().__init__("Allied Chestplate of Generosity", 10, base_duration=10)   
        embellishment_effect = caster.embellishments[self.name]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -self.embellishment_first_value)
    
    
class AlliedWristguardOfCompanionship(Buff):
    
    def __init__(self, caster):
        super().__init__("Allied Wristguards of Companionship", 10000, base_duration=10000)   
        embellishment_effect = caster.embellishments["Allied Wristgaurds of Companionship"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        targets_nearby = 4
        self.embellishment_first_value = embellishment_values[0] * targets_nearby
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -self.embellishment_first_value)
    
    
class VerdantTether(Buff):
    
    BASE_PPM = 2.2
    
    def __init__(self, caster):
        super().__init__("Verdant Tether", 15, base_duration=15)
        embellishment_effect = caster.embellishments[self.name]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        self.embellishment_second_value = embellishment_values[1]
        
        average_value = 0.75
        self.embellishment_second_value *= average_value
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.embellishment_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -self.embellishment_second_value)
    

class VerdantConduit(Buff):
    
    # 10s icd
    BASE_PPM = 5
    
    def __init__(self, caster):
        super().__init__("Verdant Conduit", 10, base_duration=10)
        embellishment_effect = caster.embellishments[self.name]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        self.chosen_stat = ""
        
    def apply_effect(self, caster, current_time=None):
        self.chosen_stat = random.choice(["haste", "crit", "mastery", "versatility"])
        caster.update_stat(self.chosen_stat, self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat(self.chosen_stat, -self.embellishment_first_value)
    

class DreamtendersCharm(Buff):
    
    def __init__(self, caster):
        super().__init__("Dreamtender's Charm", 10000, base_duration=10000, current_stacks=1, max_stacks=20)
        self.stacks_to_apply = 1
        embellishment_effect = caster.embellishments[self.name]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        caster.time_based_stacking_buffs[self] = 1
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.embellishment_first_value * self.current_stacks)
    
    
class DarkmoonSigilAscension(Buff):
    
    def __init__(self, caster):
        super().__init__("Darkmoon Sigil: Ascension", 10000, base_duration=10000, current_stacks=1, max_stacks=11)
        self.stacks_to_apply = 1
        embellishment_effect = caster.embellishments["Ascendance"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        self.first_stack = True
        self.first_time_reaching_ten_stacks = True
        
        self.embellishment_first_value = 89
        if "Writhing Armor Banding" in caster.embellishments:
            self.embellishment_first_value *= 2
        caster.time_based_stacking_buffs[self] = 8
        
        self.chosen_stat = None
        
    def apply_effect(self, caster, current_time=None):
        if self.chosen_stat and self.current_stacks == 10:
            caster.update_stat(self.chosen_stat, -self.embellishment_first_value * (self.current_stacks))
        elif self.chosen_stat:
            caster.update_stat(self.chosen_stat, -self.embellishment_first_value * self.current_stacks)
            
        if self.first_time_reaching_ten_stacks:
            caster.update_stat(self.chosen_stat, self.embellishment_first_value)
            self.first_time_reaching_ten_stacks = False
        
        available_stats = ["haste", "crit", "mastery", "versatility"]
        if self.chosen_stat in available_stats:
            available_stats.remove(self.chosen_stat)
        
        self.chosen_stat = random.choice(available_stats)
        if self.current_stacks == 10:
            caster.update_stat(self.chosen_stat, self.embellishment_first_value * (self.current_stacks))
        else:
            caster.update_stat(self.chosen_stat, self.embellishment_first_value * (self.current_stacks + 1))
            
        
        if self.current_stacks == 1 and self.first_stack:
            caster.update_stat(self.chosen_stat, -self.embellishment_first_value * (self.current_stacks + 1))
            self.current_stacks -= 1
            self.first_stack = False
            
        if self.current_stacks == 10:
            self.current_stacks -= 1
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat(self.chosen_stat, -self.embellishment_first_value * self.current_stacks)
    

class DarkmoonSigilSymbiosis(Buff):
    
    def __init__(self, caster):
        super().__init__("Darkmoon Sigil: Symbiosis", 10000, base_duration=10000, current_stacks=1, max_stacks=5)
        self.stacks_to_apply = 1
        embellishment_effect = caster.embellishments["Symbiosis"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = 131
        if "Writhing Armor Banding" in caster.embellishments:
            self.embellishment_first_value *= 2
        caster.time_based_stacking_buffs[self] = 10
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.embellishment_first_value * self.current_stacks)
        

class DarkmoonDeckSymbiosis(Buff):
    
    def __init__(self, caster):
        super().__init__("Darkmoon Deck: Symbiosis", 10000, base_duration=10000, current_stacks=1, max_stacks=5)
        self.stacks_to_apply = 1
        trinket_effect = caster.trinkets["Darkmoon Deck: Symbiosis"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        
        caster.time_based_stacking_buffs[self] = 10
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.trinket_first_value * self.current_stacks)
        

class MagazineOfHealingDarts(Buff):
    
    def __init__(self, caster):
        super().__init__("Dreamtender's Charm", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class BronzedGripWrappings(Buff):
    
    def __init__(self, caster):
        super().__init__("Dreamtender's Charm", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
   
    
class DawnlightAvailable(Buff):
    
    def __init__(self, caster):
        super().__init__("Dawnlight", 30, base_duration=30, current_stacks=2, max_stacks=2)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass


class LightOfTheMartyrBuff(Buff):
    
    def __init__(self, caster, duration_to_apply):
        super().__init__("Light of the Martyr", duration_to_apply, base_duration=duration_to_apply)
        # caster.time_based_stacking_buffs[self] = duration_to_apply
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        if "Bestow Light" in caster.active_auras:
            del caster.active_auras["Bestow Light"]
            update_self_buff_data(caster.self_buff_breakdown, "Bestow Light", current_time, "expired") 
            
            for buff in caster.time_based_stacking_buffs:
                if buff.name == "Bestow Light":
                    del caster.time_based_stacking_buffs[buff]
                    return
    

class BestowLight(Buff):
    
    def __init__(self, caster, duration_to_apply):
        super().__init__("Bestow Light", 10000, base_duration=10000, current_stacks=1, max_stacks=3)
        self.stacks_to_apply = 1
        caster.time_based_stacking_buffs[self] = 5
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class MorningStar(Buff):
    
    def __init__(self, caster):
        super().__init__("Morning Star", 10000, base_duration=10000, current_stacks=10, max_stacks=10)
        self.stacks_to_apply = 1
        caster.time_based_stacking_buffs[self] = 5
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class GleamingRays(Buff):
    
    def __init__(self, caster):
        super().__init__("Gleaming Rays", 8, base_duration=8)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class BlessingOfAnshe(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Blessing of An'she", 20, base_duration=20)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class SolarGrace(Buff):
    count = 0

    def __init__(self, caster):
        SolarGrace.count += 1
        self.count = SolarGrace.count
        
        if SolarGrace.count == 6:
            SolarGrace.count = 0
        super().__init__(f"Solar Grace {self.count}", 12, base_duration=12)  
        
    def apply_effect(self, caster, current_time=None):
        # if additive
        # caster.flat_haste -= 3 * self.active_solar_graces
        # self.active_solar_graces += 1
        # caster.flat_haste += 3 * self.active_solar_graces
        # caster.update_stat("haste", 0)
        
        current_stacks = len([buff for buff in caster.active_auras.values() if "Solar Grace" in buff.name])
        current_stacks_multiplier = ((pow(1.02, current_stacks)) - 1) * 100
        
        new_stacks = current_stacks + 1
        new_stacks_multiplier = ((pow(1.02, new_stacks)) - 1) * 100
        
        # update_stat_with_multiplicative_percentage(caster, "haste", 3 * (len([buff for buff in caster.active_auras.values() if "Solar Grace" in buff.name]) - 1), False)
        # update_stat_with_multiplicative_percentage(caster, "haste", 3 * (len([buff for buff in caster.active_auras.values() if "Solar Grace" in buff.name])), True)
        
        update_stat_with_multiplicative_percentage(caster, "haste", current_stacks_multiplier, False)
        update_stat_with_multiplicative_percentage(caster, "haste", new_stacks_multiplier, True)
        
        caster.update_hasted_cooldowns_with_haste_changes()
        
    def remove_effect(self, caster, current_time=None):
        # caster.flat_haste -= 3
        # caster.update_stat("haste", 0)
        
        # update_stat_with_multiplicative_percentage(caster, "haste", 3 * (len([buff for buff in caster.active_auras.values() if "Solar Grace" in buff.name])), False)
        # update_stat_with_multiplicative_percentage(caster, "haste", 3 * (len([buff for buff in caster.active_auras.values() if "Solar Grace" in buff.name]) - 1), True)
        
        current_stacks = len([buff for buff in caster.active_auras.values() if "Solar Grace" in buff.name])
        current_stacks_multiplier = ((pow(1.02, current_stacks)) - 1) * 100
        
        new_stacks = current_stacks - 1
        new_stacks_multiplier = ((pow(1.02, new_stacks)) - 1) * 100
        
        update_stat_with_multiplicative_percentage(caster, "haste", current_stacks_multiplier, False)
        update_stat_with_multiplicative_percentage(caster, "haste", new_stacks_multiplier, True)
        caster.update_hasted_cooldowns_with_haste_changes()
    

class SacredWeaponBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Sacred Weapon", 20, base_duration=20)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class HolyBulwarkSelf(Buff):
    
    def __init__(self, caster):
        super().__init__("Holy Bulwark", 20, base_duration=20)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class SacredWeaponSelf(Buff):
    
    def __init__(self, caster):
        super().__init__("Sacred Weapon", 20, base_duration=20)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class RiteOfSanctification(Buff):
    
    def __init__(self, caster):
        super().__init__("Rite of Sanctification", 10000, base_duration=10000)   
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power *= 1.01
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power /= 1.01
        

class RiteOfAdjurationBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Rite of Adjuration", 10000, base_duration=10000)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class SunsAvatar(Buff):
    
    def __init__(self, caster):
        super().__init__("Sun's Avatar", 8, base_duration=8)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class SunsAvatarActive(Buff):
        
    def __init__(self, caster):
        super().__init__("Sun's Avatar Active", 10000, base_duration=10000)   
        self.timer = 0
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    def trigger_passive_heal(self, caster, current_time, target_count):
        from .spells_healing import SunsAvatarHeal
    
        targets = random.choices(caster.potential_healing_targets, k=target_count)
        for target in targets:            
            suns_avatar_heal, suns_avatar_crit = SunsAvatarHeal(caster).calculate_heal(caster)

            target.receive_heal(suns_avatar_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Sun's Avatar", target, suns_avatar_heal, suns_avatar_crit)
            
            caster.handle_beacon_healing("Sun's Avatar", target, suns_avatar_heal, current_time)
        
    
class BlessedAssurance(Buff):
    
    def __init__(self, caster):
        super().__init__("Blessed Assurance", 10000, base_duration=10000)   
            
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class DivineGuidance(Buff):
    
    def __init__(self, caster):
        super().__init__("Divine Guidance", 10000, base_duration=10000, current_stacks=1, max_stacks=10)   
            
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        from .spells_healing import DivineGuidanceHeal
        
        divine_guidance_stacks = caster.active_auras["Divine Guidance"].current_stacks
        divine_guidance_heal, divine_guidance_crit = DivineGuidanceHeal(caster).calculate_heal(caster)
        divine_guidance_heal *= divine_guidance_stacks
        
        if divine_guidance_crit:
            divine_guidance_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
        divine_guidance_heal = add_talent_healing_multipliers(divine_guidance_heal, caster)
        divine_guidance_heal /= 5
        
        chosen_targets = random.sample(caster.potential_healing_targets, 5)
        for target in chosen_targets:
            target.receive_heal(divine_guidance_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Divine Guidance", target, divine_guidance_heal, divine_guidance_crit)
            

class PureLight(Buff):
    
    def __init__(self, caster):
        super().__init__("Pure Light", 30, base_duration=30, current_stacks=1, max_stacks=4)   
            
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    
class Liberation(Buff):
    
    def __init__(self, caster):
        super().__init__("Liberation", 20, base_duration=20)   
        self.mana_cost = caster.abilities["Judgment"].mana_cost * caster.base_mana
            
    def apply_effect(self, caster, current_time=None):
        caster.abilities["Judgment"].mana_cost_modifier *= 1 - (6000 / self.mana_cost)
        
    def remove_effect(self, caster, current_time=None):
        caster.abilities["Judgment"].mana_cost_modifier /= 1 - (6000 / self.mana_cost)
        

class BlessingOfTheForge(Buff):
    
    def __init__(self, caster, duration_to_apply):
        super().__init__("Blessing of the Forge", duration_to_apply, base_duration=duration_to_apply)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class AuthorityOfRadiantPower(Buff):
    
    BASE_PPM = 3
    
    def __init__(self, caster):
        super().__init__("Authority of Radiant Power", 10, base_duration=10)   
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(2230)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(2230)
        
        
class CouncilsGuile(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Council's Guile", 12, base_duration=12)   
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 3910)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -3910)
        
        
class StormridersFury(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Stormrider's Fury", 12, base_duration=12)   
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 3910)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -3910)
        

class StoneboundArtistry(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Stonebound Artistry", 12, base_duration=12)   
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 3910)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -3910)
        

class OathswornsTenacity(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Oathsworn's Tenacity", 12, base_duration=12)   
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 3910)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -3910)
        

class GaleOfShadows(Buff):
    
    def __init__(self, caster):
        super().__init__("Gale of Shadows", 15, base_duration=15, current_stacks=1, max_stacks=20)   
        trinket_effect = caster.trinkets["Gale of Shadows"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value * self.current_stacks)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value * self.current_stacks)
        

class SurekiZealotsInsignia(Buff):
    count = 0
    
    BASE_PPM = 1
    
    def __init__(self, caster):
        SurekiZealotsInsignia.count += 1
        self.count = SurekiZealotsInsignia.count
        
        if SurekiZealotsInsignia.count == caster.variable_target_counts["Sureki Zealot's Insignia"]:
            SurekiZealotsInsignia.count = 0
        super().__init__(f"Sureki Zealot's Insignia {self.count}", 10, base_duration=10)  
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 694)
        mana_gain = 6250
        caster.mana += mana_gain
        update_mana_gained(caster.ability_breakdown, "Sureki Zealot's Insignia", mana_gain)
    
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -694)
        

class PotionBombOfPower(Buff):
    
    def __init__(self, caster):
        super().__init__("Potion Bomb of Power", 30, base_duration=30)   
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(632)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(632)
        

class DawnthreadLining(Buff):
    
    def __init__(self, caster):
        super().__init__("Dawnthread Lining", 10000, base_duration=10000)   
        embellishment_effect = caster.embellishments["Dawnthread Lining"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = 756
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -self.embellishment_first_value)
        
        
class DuskthreadLining(Buff):
    
    def __init__(self, caster):
        super().__init__("Duskthread Lining", 10000, base_duration=10000)   
        embellishment_effect = caster.embellishments["Duskthread Lining"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = 756
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.embellishment_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -self.embellishment_first_value)
        
        
class PrismaticNullStone(Buff):
    
    def __init__(self, caster):
        super().__init__("Prismatic Null Stone", 10000, base_duration=10000)   
        
    def apply_effect(self, caster, current_time=None):
        unique_gem_colours = sum(1 for gem in ["Emerald", "Sapphire", "Onyx", "Ruby"] if caster.gem_counts[gem] > 0)
        
        if "Insightful Blasphemite" in caster.gems:
            caster.max_mana = caster.mana + caster.base_mana * unique_gem_colours * 0.0025
            caster.mana = caster.max_mana
            
        if "Culminating Blasphemite" in caster.gems:
            caster.crit_healing_modifier += unique_gem_colours * 0.0015 * 0.25
            caster.base_crit_healing_modifier += unique_gem_colours * 0.0015 * 0.25
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class WrithingArmorBanding(Buff):
    
    def __init__(self, caster):
        super().__init__("Writhing Armor Banding", 10000, base_duration=10000)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class EnergyRedistributionBeacon(Buff):
    
    def __init__(self, caster):
        super().__init__("Energy Redistribution Beacon", 10000, base_duration=10000)   
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    
class BlessedWeaponGrip(Buff):
    
    BASE_PPM = 1
    
    def __init__(self, caster):
        super().__init__("Blessed Weapon Grip", 30, base_duration=30, current_stacks=10, max_stacks=10)   
        embellishment_effect = caster.embellishments["Blessed Weapon Grip"]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = 185
        self.highest_stat = caster.find_highest_secondary_stat_rating()
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat(self.highest_stat, self.embellishment_first_value * self.current_stacks)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat(self.highest_stat, -self.embellishment_first_value * self.current_stacks)
        

class SpymastersWebStacks(Buff):
    
    def __init__(self, caster):
        super().__init__("Spymaster's Web Stacks", 10000, base_duration=10000, current_stacks=1, max_stacks=40)   
        trinket_effect = caster.trinkets["Spymaster's Web"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*?(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value * self.current_stacks)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value * self.current_stacks)
    

class SpymastersWebBuff(Buff):
        
    def __init__(self, caster):
        super().__init__("Spymaster's Web", 20, base_duration=20)   
        trinket_effect = caster.trinkets["Spymaster's Web"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_second_value = trinket_values[1]
        self.stack_count = 0
        
    def apply_effect(self, caster, current_time=None):
        self.stack_count = caster.active_auras["Spymaster's Web Stacks"].current_stacks
        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_second_value * self.stack_count)
        
        caster.active_auras["Spymaster's Web Stacks"].remove_effect(caster)
        del caster.active_auras["Spymaster's Web Stacks"]
        update_self_buff_data(caster.self_buff_breakdown, "Spymaster's Web Stacks", current_time, "expired")
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_second_value * self.stack_count)
        self.stack_count = 0