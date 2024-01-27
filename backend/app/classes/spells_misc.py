from .spells import Spell
from ..utils.misc_functions import increment_holy_power, update_spell_holy_power_gain


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