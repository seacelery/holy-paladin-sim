import re

from .spells import Spell
from .auras_buffs import MirrorOfFracturedTomorrowsBuff, SmolderingSeedlingActive, NymuesUnravelingSpindleBuff
from ..utils.misc_functions import update_mana_gained


class Trinket(Spell):
    
    def __init__(self, name, cooldown=0, off_gcd=True, base_cast_time=0):
        super().__init__(name, cooldown=cooldown, off_gcd=off_gcd, base_cast_time=base_cast_time)
    
    
class MirrorOfFracturedTomorrows(Trinket):
    
    BASE_COOLDOWN = 180
    
    def __init__(self, caster):
        super().__init__("Mirror of Fractured Tomorrows", cooldown=MirrorOfFracturedTomorrows.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(MirrorOfFracturedTomorrowsBuff(caster), current_time)
            

class EchoingTyrstone(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Echoing Tyrstone Cast", cooldown=EchoingTyrstone.BASE_COOLDOWN, off_gcd=True)
        self.tyrstone_start_time = 0
        self.tyrstone_end_time = 0
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            self.tyrstone_start_time = current_time
            self.tyrstone_end_time = current_time + 10
            

class SmolderingSeedling(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Smoldering Seedling", cooldown=SmolderingSeedling.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(SmolderingSeedlingActive(caster), current_time)
            
            
class NymuesUnravelingSpindle(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Nymue's Unraveling Spindle", cooldown=NymuesUnravelingSpindle.BASE_COOLDOWN, off_gcd=True, base_cast_time=3)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(NymuesUnravelingSpindleBuff(caster), current_time)
            

class ConjuredChillglobe(Trinket):
    
    BASE_COOLDOWN = 60
    
    def __init__(self, caster):
        super().__init__("Conjured Chillglobe", cooldown=ConjuredChillglobe.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            trinket_effect = caster.trinkets[self.name]["effect"]
            trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
            
            # damage
            self.trinket_first_value = trinket_values[0]
            # mana gain
            self.trinket_second_value = trinket_values[1]
            
            if caster.mana > caster.max_mana * 0.65:
                pass
            else:
                caster.mana += self.trinket_second_value
                update_mana_gained(caster.ability_breakdown, self.name, self.trinket_second_value)
                

class TimeBreachingTalon(Trinket):
    
    BASE_COOLDOWN = 150
    
    def __init__(self, caster):
        super().__init__("Time-Breaching Talon", cooldown=TimeBreachingTalon.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            from .auras_buffs import TimeBreachingTalonPlus
            
            caster.apply_buff_to_self(TimeBreachingTalonPlus(caster), current_time)
            

class SpoilsOfNeltharus(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Spoils of Neltharus", cooldown=SpoilsOfNeltharus.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            from .auras_buffs import SpoilsOfNeltharusBuff
            
            caster.apply_buff_to_self(SpoilsOfNeltharusBuff(caster), current_time)