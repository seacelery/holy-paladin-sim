from spells import Spell

# PASSIVE SPELLS
class GlimmerOfLightSpell(Spell):
    # glorious dawn multiplier
    SPELL_POWER_COEFFICIENT = 1.6416 * 1.1
    
    def __init__(self, caster):
        super().__init__("Glimmer of Light")
        
    def cast_healing_spell(self):
        pass
    
class JudgmentOfLightSpell(Spell):
    SPELL_POWER_COEFFICIENT = 0.175
    
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
        