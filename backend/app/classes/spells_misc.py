from .spells import Spell
from .auras_buffs import ElementalPotionOfUltimatePowerBuff, AuraMasteryBuff, TemperedPotionBuff, SlumberingSoulSerumBuff
from ..utils.misc_functions import increment_holy_power, update_mana_gained


class AuraMastery(Spell):
    
    BASE_COOLDOWN = 180
    
    def __init__(self, caster):
        super().__init__("Aura Mastery", cooldown=AuraMastery.BASE_COOLDOWN)
        if caster.is_talent_active("Unwavering Spirit"):
            self.cooldown -= 30
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(AuraMasteryBuff(), current_time)


class ArcaneTorrent(Spell):
    
    HOLY_POWER_GAIN = 1
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Arcane Torrent", cooldown=ArcaneTorrent.BASE_COOLDOWN, holy_power_gain=ArcaneTorrent.HOLY_POWER_GAIN)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            increment_holy_power(self, caster, current_time)
        
   
class Potion(Spell):
    
    BASE_COOLDOWN = 300
    shared_cooldown_end_time = 0
    
    def __init__(self, name):
        super().__init__(name, cooldown=Potion.BASE_COOLDOWN, off_gcd=True)
        
    def check_potion_cooldown(self, caster, current_time):
        return current_time >= caster.abilities["Potion"].shared_cooldown_end_time
        
        
class AeratedManaPotion(Potion):

    def __init__(self, caster):
        super().__init__("Aerated Mana Potion")
        Potion.shared_cooldown_end_time = 0
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            aerated_mana_potion_mana_gain = 27600
            caster.mana += aerated_mana_potion_mana_gain
            update_mana_gained(caster.ability_breakdown, self.name, aerated_mana_potion_mana_gain)
            
            Potion.shared_cooldown_end_time = current_time + self.cooldown
            
            
class ElementalPotionOfUltimatePowerPotion(Potion):

    def __init__(self, caster):
        super().__init__("Elemental Potion of Ultimate Power")
        Potion.shared_cooldown_end_time = 0
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(ElementalPotionOfUltimatePowerBuff(caster), current_time)
            
            Potion.shared_cooldown_end_time = current_time + self.cooldown
            

# ptr
class AlgariManaPotion(Potion):
    
    def __init__(self, caster):
        super().__init__("Algari Mana Potion")
        Potion.shared_cooldown_end_time = 0
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            algari_mana_potion_mana_gain = 150000
            caster.mana += algari_mana_potion_mana_gain
            update_mana_gained(caster.ability_breakdown, self.name, algari_mana_potion_mana_gain)
            
            Potion.shared_cooldown_end_time = current_time + self.cooldown
            
            
class SlumberingSoulSerum(Potion):
    
    def __init__(self, caster):
        super().__init__("Slumbering Soul Serum")
        Potion.shared_cooldown_end_time = 0
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(SlumberingSoulSerumBuff(caster), current_time)
            
            Potion.shared_cooldown_end_time = current_time + self.cooldown
            

class TemperedPotion(Potion):
    
    def __init__(self, caster):
        super().__init__("Tempered Potion")
        Potion.shared_cooldown_end_time = 0
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(TemperedPotionBuff(caster), current_time)
            
            Potion.shared_cooldown_end_time = current_time + self.cooldown