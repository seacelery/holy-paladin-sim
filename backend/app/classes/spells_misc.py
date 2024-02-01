from .spells import Spell
from .auras_buffs import ElementalPotionOfUltimatePowerBuff
from ..utils.misc_functions import increment_holy_power, update_spell_holy_power_gain, update_mana_gained


class ArcaneTorrent(Spell):
    
    SPELL_ID = 155145
    HOLY_POWER_GAIN = 1
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Arcane Torrent", cooldown=ArcaneTorrent.BASE_COOLDOWN, holy_power_gain=ArcaneTorrent.HOLY_POWER_GAIN)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            pass
        
   
class Potion(Spell):
    
    BASE_COOLDOWN = 300
    shared_cooldown_end_time = 0
    
    def __init__(self, name):
        super().__init__(name, cooldown=Potion.BASE_COOLDOWN, off_gcd=True)
        
    def check_potion_cooldown(self, current_time):
        return current_time >= Potion.shared_cooldown_end_time
        
        
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
            caster.apply_buff_to_self(ElementalPotionOfUltimatePowerBuff(), current_time)
            
            Potion.shared_cooldown_end_time = current_time + self.cooldown
            