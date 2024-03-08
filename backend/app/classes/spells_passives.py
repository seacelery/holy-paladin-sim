from .spells import Spell

# PASSIVE SPELLS


class GlimmerOfLightSpell(Spell):
    
    # glorious dawn multiplier
    SPELL_ID = 287269
    SPELL_POWER_COEFFICIENT = 1.6416 * 1.1
    
    def __init__(self, caster):
        super().__init__("Glimmer of Light")
        
    def cast_healing_spell(self):
        pass
    
    
class JudgmentOfLightSpell(Spell):
    
    SPELL_ID = 183778
    SPELL_POWER_COEFFICIENT = 0.175
    
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