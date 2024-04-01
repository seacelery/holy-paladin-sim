import random


class Summon:
    
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        
    def apply_effect(self, caster):
        pass
    
    def remove_effect(self, caster):
        pass
        
        
class LightsHammerSummon(Summon):
    
    def __init__(self):
        super().__init__("Light's Hammer", 14)
        self.last_tick_time = 0
        self.base_tick_interval = 2 
        
    def apply_effect(self, caster, current_time):
        self.last_tick_time = 0
        
        # trigger first tick at 0s
        self.trigger_lights_hammer_tick(caster, current_time)
        
    def increment_lights_hammer(self, caster, current_time, tick_rate):
        self.last_tick_time += tick_rate
        if self.last_tick_time >= self.base_tick_interval - 0.001:
            self.trigger_lights_hammer_tick(caster, current_time)
            self.last_tick_time = 0
            
    def trigger_lights_hammer_tick(self, caster, current_time):
        from .spells_healing import LightsHammerHeal
        
        targets = []
        for _ in range(LightsHammerHeal(caster).TARGET_COUNT):
            targets.append(random.choice(caster.potential_healing_targets))
        LightsHammerHeal(caster).cast_healing_spell(caster, targets, current_time, is_heal=True)
            

class ConsecrationSummon(Summon):
    
    def __init__(self):
        super().__init__("Consecration", 12)
        self.last_tick_time = 0
        self.base_tick_interval = 1
        
    def apply_effect(self, caster, current_time):
        self.last_tick_time = 0
        
        # trigger first tick at 0s
        # golden path
        if caster.is_talent_active("Golden Path"):
            self.trigger_golden_path_tick(caster, current_time)
        
    def increment_consecration(self, caster, current_time, tick_rate):
        self.last_tick_time += tick_rate
        if self.last_tick_time >= self.base_tick_interval - 0.001:
            # golden path
            if caster.is_talent_active("Golden Path"):
                self.trigger_golden_path_tick(caster, current_time)
            self.last_tick_time = 0
            
    def trigger_golden_path_tick(self, caster, current_time):
        from .spells_healing import GoldenPathHeal
        
        targets = []
        for _ in range(GoldenPathHeal(caster).TARGET_COUNT):
            targets.append(random.choice(caster.potential_healing_targets))
            
        GoldenPathHeal(caster).cast_healing_spell(caster, targets, current_time, is_heal=True)
        
        # seal of mercy
        if caster.is_talent_active("Seal of Mercy"):
            self.trigger_seal_of_mercy_tick(caster, current_time, targets)
        
    def trigger_seal_of_mercy_tick(self, caster, current_time, targets):
        from .spells_healing import SealOfMercyHeal
        
        target = [random.choice(targets)]
        
        SealOfMercyHeal(caster).cast_healing_spell(caster, target, current_time, is_heal=True)
        
        
class RighteousJudgmentSummon(Summon):
    
    def __init__(self, caster):
        caster.extra_consecration_count += 1
        super().__init__(f"Consecration (Righteous Judgment) {caster.extra_consecration_count}", 12)
        self.last_tick_time = 0
        self.base_tick_interval = 1
        
    def apply_effect(self, caster, current_time):
        self.last_tick_time = 0
        
        # trigger first tick at 0s
        # golden path
        if caster.is_talent_active("Golden Path"):
            self.trigger_golden_path_tick(caster, current_time)
        
    def increment_consecration(self, caster, current_time, tick_rate):
        self.last_tick_time += tick_rate
        if self.last_tick_time >= self.base_tick_interval - 0.001:
            # golden path
            if caster.is_talent_active("Golden Path"):
                self.trigger_golden_path_tick(caster, current_time)
            self.last_tick_time = 0
            
    def trigger_golden_path_tick(self, caster, current_time):
        from .spells_healing import GoldenPathHeal
        
        targets = []
        for _ in range(GoldenPathHeal(caster).TARGET_COUNT):
            targets.append(random.choice(caster.potential_healing_targets))
            
        GoldenPathHeal(caster).cast_healing_spell(caster, targets, current_time, is_heal=True)
        
        # seal of mercy
        if caster.is_talent_active("Seal of Mercy"):
            self.trigger_seal_of_mercy_tick(caster, current_time, targets)
        
    def trigger_seal_of_mercy_tick(self, caster, current_time, targets):
        from .spells_healing import SealOfMercyHeal
        
        target = [random.choice(targets)]
        
        SealOfMercyHeal(caster).cast_healing_spell(caster, target, current_time, is_heal=True)