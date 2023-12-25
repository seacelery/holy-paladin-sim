import random
from misc_functions import append_spell_heal_event, format_time

class Aura:
    def __init__(self, name, duration, base_duration=0, current_stacks=1, max_stacks=1):
        self.name = name
        self.duration = duration
        self.base_duration = base_duration
        self.current_stacks = current_stacks
        self.max_stacks = max_stacks
        
    def apply_effect(self, caster):
        pass
    
    def remove_effect(self, caster):
        pass

class Buff(Aura):
    def __init__(self, name, duration, base_duration=0, current_stacks=1, max_stacks=1):
        super().__init__(name, duration, base_duration, current_stacks=current_stacks, max_stacks=max_stacks) 
    
class Debuff(Aura):
    def __init__(self, name, duration, base_duration=0, current_stacks=1, max_stacks=1):
        super().__init__(name, duration, base_duration, current_stacks=current_stacks, max_stacks=max_stacks) 
    

