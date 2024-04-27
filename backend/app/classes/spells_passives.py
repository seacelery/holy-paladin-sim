import random
import re

from .spells import Spell
from ..utils.misc_functions import update_spell_data_heals, add_talent_healing_multipliers


# PASSIVE SPELLS
class GlimmerOfLightSpell(Spell):
    
    SPELL_POWER_COEFFICIENT = 1.6416 * 0.8
    
    def __init__(self, caster):
        super().__init__("Glimmer of Light")
        
    def cast_healing_spell(self):
        pass
    
    
class JudgmentOfLightSpell(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.175 * 0.8
    
    def __init__(self, caster):
        super().__init__("Judgment of Light")


class GreaterJudgmentSpell(Spell):
    
    SPELL_POWER_COEFFICIENT = 1.84
    
    def __init__(self, caster):
        super().__init__("Greater Judgment", is_absorb=True)
        
        
class TouchOfLight(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.45 * 5
    BASE_PPM = 3
    
    def __init__(self, caster):
        super().__init__("Touch of Light")
        

class ChirpingRune(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    BASE_PPM = 6
    
    def __init__(self, caster):
        super().__init__("Chirping Rune")
        
    def apply_flat_healing(self, caster, target, current_time, is_heal):     
        chirping_rune_heal, chirping_rune_crit = ChirpingRune(caster).calculate_heal(caster)
        chirping_rune_heal = 7987 * caster.versatility_multiplier
        
        if chirping_rune_crit:
            chirping_rune_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
        chirping_rune_heal = add_talent_healing_multipliers(chirping_rune_heal, caster)
        
        target.receive_heal(chirping_rune_heal, caster)
        update_spell_data_heals(caster.ability_breakdown, "Chirping Rune", target, chirping_rune_heal, chirping_rune_crit)
        

class DreamingDevotion(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    BASE_PPM = 3
    
    def __init__(self, caster):
        super().__init__("Dreaming Devotion")
        
    def apply_flat_healing(self, caster, targets, current_time, is_heal):
        chosen_target = targets
        secondary_targets = random.sample([target for target in caster.potential_healing_targets if target != chosen_target], random.randint(10, 19))
        
        chosen_targets = [chosen_target] + secondary_targets
        
        for target in chosen_targets:
            dreaming_devotion_heal, dreaming_devotion_crit = DreamingDevotion(caster).calculate_heal(caster)
            dreaming_devotion_heal = 16826 * caster.versatility_multiplier
            
            if dreaming_devotion_crit:
                dreaming_devotion_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
                
            dreaming_devotion_heal = add_talent_healing_multipliers(dreaming_devotion_heal, caster)
            
            target.receive_heal(dreaming_devotion_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Dreaming Devotion", target, dreaming_devotion_heal, dreaming_devotion_crit)
            

class LarodarsFieryReverie(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    BASE_PPM = 1
    
    def __init__(self, caster):
        super().__init__("Larodar's Fiery Reverie")
        
    def apply_flat_healing(self, caster, target, current_time, is_heal):     
        larodars_fiery_reverie_heal, larodars_fiery_reverie_crit = LarodarsFieryReverie(caster).calculate_heal(caster)
        scaled_larodars_fiery_reverie_heal = (314488 / pow(1.014, 528)) * pow(1.014, caster.equipment["head"]["item_level"])
        
        larodars_fiery_reverie_heal = scaled_larodars_fiery_reverie_heal * caster.versatility_multiplier
        
        if larodars_fiery_reverie_crit:
            larodars_fiery_reverie_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
        larodars_fiery_reverie_heal = add_talent_healing_multipliers(larodars_fiery_reverie_heal, caster)
        
        target.receive_heal(larodars_fiery_reverie_heal, caster)
        update_spell_data_heals(caster.ability_breakdown, "Larodar's Fiery Reverie", target, larodars_fiery_reverie_heal, larodars_fiery_reverie_crit)
 
 
class EmbraceOfAkunda(Spell):
    
    SPELL_POWER_COEFFICIENT = 1.04 * 0.66
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Embrace of Akunda")
        
   
# Mirror of Fractured Tomorrows trinket healing cast     
class RestorativeSands(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    
    def __init__(self, caster):
        super().__init__("Restorative Sands")
        

# Rashok's Molten Heart heal
class RashoksMoltenHeartHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    
    def __init__(self, caster):
        super().__init__("Rashok's Molten Heart")
        
        
# Echoing Tyrstone conditional proc
class EchoingTyrstoneProc(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    AVERAGE_TIME_TO_PROC = 20
    
    def __init__(self, caster):
        super().__init__("Echoing Tyrstone")
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # flat healing
        self.trinket_first_value = trinket_values[0]
        # haste
        self.trinket_second_value = trinket_values[1]
        
    def trigger_proc(self, caster, targets, current_time):
        from .auras_buffs import EchoingTyrstoneBuff
        target_count = 5
        
        for i in range(target_count):
            target = random.choice(caster.potential_healing_targets)
            
            echoing_tyrstone_heal, echoing_tyrstone_crit = EchoingTyrstoneProc(caster).calculate_heal(caster)
            echoing_tyrstone_heal = self.trinket_first_value / target_count
            if echoing_tyrstone_crit:
                echoing_tyrstone_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
            target.receive_heal(echoing_tyrstone_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Echoing Tyrstone", target, echoing_tyrstone_heal, echoing_tyrstone_crit)
            
        caster.apply_buff_to_self(EchoingTyrstoneBuff(caster), current_time)
        
        
# Blossom of Amirdrassil conditional proc
class BlossomOfAmirdrassilProc(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    AVERAGE_TIME_TO_PROC = 5
    BASE_COOLDOWN = 60
    
    def __init__(self, caster):
        super().__init__("Blossom of Amirdrassil")
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # initial hot
        self.trinket_first_value = trinket_values[0]
        # three target hot
        self.trinket_second_value = trinket_values[1]
        # absorb
        self.trinket_third_value = trinket_values[2]
        
    def trigger_proc(self, caster, targets, current_time):
        from .auras_buffs import BlossomOfAmirdrassilLargeHoT, BlossomOfAmirdrassilSmallHoT
        
        random.choice(caster.potential_healing_targets)
        target = targets[0]
        target.apply_buff_to_target(BlossomOfAmirdrassilLargeHoT(caster), current_time, caster=caster)
        
        if random.random() > 0.1:
            chosen_targets = random.sample(caster.potential_healing_targets, 3)
            for target in chosen_targets:
                target.apply_buff_to_target(BlossomOfAmirdrassilSmallHoT(caster), current_time, caster=caster)
        else:
            absorb_amount = self.trinket_third_value * caster.versatility_multiplier
            target.receive_heal(absorb_amount, caster)
            update_spell_data_heals(caster.ability_breakdown, "Blossom of Amirdrassil Absorb", target, absorb_amount, False)
            
        update_spell_data_heals(caster.ability_breakdown, "Blossom of Amirdrassil", target, 0, False)
        

# embellishments
class MagazineOfHealingDarts(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Magazine of Healing Darts")
        embellishment_effect = caster.embellishments[self.name]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        
    def apply_flat_healing(self, caster, target, current_time, is_heal):     
        healing_dart_heal, healing_dart_crit = MagazineOfHealingDarts(caster).calculate_heal(caster)
        healing_dart_heal = self.embellishment_first_value * caster.versatility_multiplier
        
        if healing_dart_crit:
            healing_dart_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
        healing_dart_heal = add_talent_healing_multipliers(healing_dart_heal, caster)
        
        target.receive_heal(healing_dart_heal, caster)
        update_spell_data_heals(caster.ability_breakdown, "Magazine of Healing Darts", target, healing_dart_heal, healing_dart_crit)
        
        
class BronzedGripWrappings(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    # base 4 ppm shared with damage proc
    BASE_PPM = 3
    
    def __init__(self, caster):
        super().__init__("Bronzed Grip Wrappings")
        embellishment_effect = caster.embellishments[self.name]["effect"]
        embellishment_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", embellishment_effect)]
        
        self.embellishment_first_value = embellishment_values[0]
        
    def apply_flat_healing(self, caster, target, current_time, is_heal):     
        bronzed_grip_wrappings_heal, bronzed_grip_wrappings_crit = BronzedGripWrappings(caster).calculate_heal(caster)
        bronzed_grip_wrappings_heal = self.embellishment_first_value * caster.versatility_multiplier
        
        if bronzed_grip_wrappings_crit:
            bronzed_grip_wrappings_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
        bronzed_grip_wrappings_heal = add_talent_healing_multipliers(bronzed_grip_wrappings_heal, caster)
        
        target.receive_heal(bronzed_grip_wrappings_heal, caster)
        update_spell_data_heals(caster.ability_breakdown, "Bronzed Grip Wrappings", target, bronzed_grip_wrappings_heal, bronzed_grip_wrappings_crit)