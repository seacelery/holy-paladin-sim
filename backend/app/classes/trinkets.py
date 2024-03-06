from .spells import Spell
from .auras_buffs import MirrorOfFracturedTomorrowsBuff


class Trinket(Spell):
    
    def __init__(self, name, cooldown=0, off_gcd=True):
        super().__init__(name, cooldown=cooldown, off_gcd=off_gcd)
    
    
class MirrorOfFracturedTomorrows(Trinket):
    # TODO clone healing
    
    BASE_COOLDOWN = 180
    
    def __init__(self, caster):
        super().__init__("Mirror of Fractured Tomorrows", cooldown=MirrorOfFracturedTomorrows.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(MirrorOfFracturedTomorrowsBuff(caster), current_time)