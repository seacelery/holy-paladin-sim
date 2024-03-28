import random
import re

from .spells import Spell
from ..utils.misc_functions import update_spell_data_heals

# PASSIVE SPELLS


class GlimmerOfLightSpell(Spell):
    
    # glorious dawn multiplier
    SPELL_ID = 287269
    SPELL_POWER_COEFFICIENT = 1.6416 * 0.8
    
    def __init__(self, caster):
        super().__init__("Glimmer of Light")
        
    def cast_healing_spell(self):
        pass
    
    
class JudgmentOfLightSpell(Spell):
    
    SPELL_ID = 183778
    SPELL_POWER_COEFFICIENT = 0.175 * 0.8
    
    def __init__(self, caster):
        super().__init__("Judgment of Light")


class GreaterJudgmentSpell(Spell):
    
    SPELL_ID = 231644
    SPELL_POWER_COEFFICIENT = 1.84
    
    def __init__(self, caster):
        super().__init__("Greater Judgment", is_absorb=True)
        
        
class TouchOfLight(Spell):
    
    SPELL_ID = 385349
    SPELL_POWER_COEFFICIENT = 0.45 * 5
    BASE_PPM = 3
    
    def __init__(self, caster):
        super().__init__("Touch of Light")
        

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
                
            if "Close to Heart" in caster.active_auras:
                dreaming_devotion_heal *= 1.08
            
            target.receive_heal(dreaming_devotion_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Dreaming Devotion", target, dreaming_devotion_heal, dreaming_devotion_crit)
 
 
class EmbraceOfAkunda(Spell):
    
    SPELL_ID = 292359
    SPELL_POWER_COEFFICIENT = 1.04 * 0.66
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Embrace of Akunda")
        
   
# Mirror of Fractured Tomorrows trinket healing cast     
class RestorativeSands(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    
    def __init__(self, caster):
        super().__init__("Restorative Sands")
        
        
# Echoing Tyrstone conditional proc
class EchoingTyrstoneProc(Spell):
    
    # TODO exact healing scaling
    
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
    
    # TODO exact healing scaling
    
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
        
        
class BronzedGripWrappings(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    # base 4 ppm shared with damage proc
    BASE_PPM = 3
    
    def __init__(self, caster):
        super().__init__("Bronzed Grip Wrappings")
    