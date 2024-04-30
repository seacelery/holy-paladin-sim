import re

from ..utils.misc_functions import format_time, update_target_buff_data, update_spell_data_heals

class Target:
    
    def __init__(self, name):
        self.name = name
        self.healing_received = 0
        self.beacon_healing_received = 0
        self.target_active_buffs = {}
        self.healing_taken_modifier = 1
        
    def receive_heal(self, amount, caster=None):
        self.healing_received += amount
        
    def receive_beacon_heal(self, amount):
        self.beacon_healing_received += amount
        
    def apply_buff_to_target(self, buff, current_time, stacks_to_apply=1, max_stacks=1, caster=None):
        if buff.name in ["Eternal Flame (HoT)"] and buff.name in self.target_active_buffs:
            self.target_active_buffs[buff.name][0].duration = min(self.target_active_buffs[buff.name][0].duration + buff.base_duration, self.target_active_buffs[buff.name][0].base_duration + self.target_active_buffs[buff.name][0].base_duration * 0.3)
        elif buff.name in self.target_active_buffs:
            self.target_active_buffs[buff.name].append(buff)
        else:
            self.target_active_buffs[buff.name] = [buff]
        buff.apply_effect(self, current_time)
        
        buff.times_applied += 1
        update_target_buff_data(caster.target_buff_breakdown, buff.name, current_time, "applied", self.name, buff.duration, buff.current_stacks)
   
    def reset_state(self):
        self.healing_received = 0
        self.beacon_healing_received = 0
        self.target_active_buffs = {}
        self.healing_taken_modifier = 1
        
class BeaconOfLight(Target):
    
    def __init__(self, name):
        super().__init__(name)
        self.beacon_healing_received = 0
        
    def receive_beacon_heal(self, amount):
        self.beacon_healing_received += amount
        
    def reset_state(self):
        super().reset_state()
        self.beacon_healing_received = 0
        
        
class SmolderingSeedling(Target):
    
    def __init__(self, name, caster):
        super().__init__(name)
        self.smoldering_seedling_healing_received = 0
        trinket_effect = caster.trinkets["Smoldering Seedling"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.smoldering_seedling_healing_cap = self.trinket_first_value
        
    def receive_heal(self, amount, caster=None, smoldering_heal=False):
        if not smoldering_heal:
            self.healing_received += amount
            self.receive_heal(amount * 1.5, caster, smoldering_heal=True)
        else:
            if self.smoldering_seedling_healing_received + amount > self.smoldering_seedling_healing_cap:
                amount = self.smoldering_seedling_healing_cap - self.smoldering_seedling_healing_received
                self.smoldering_seedling_healing_received = self.smoldering_seedling_healing_cap
            else:
                self.smoldering_seedling_healing_received += amount
                
            update_spell_data_heals(caster.ability_breakdown, "Smoldering Seedling", self, amount, False)
            
    def reset_state(self):
        super().reset_state()
        self.smoldering_seedling_healing_received = 0
            

class Player(Target):
    
    def __init__(self, name):
        super().__init__(name)
        self.self_healing = 0

    def reset_state(self):
        super().reset_state()
        self.self_healing = 0


class EnemyTarget(Target):
    
    def __init__(self, name):
        super().__init__(name)
        self.damage_taken = 0
        self.target_active_debuffs = {}
        
    def receive_damage(self, amount):
        self.damage_taken += amount
        
    def apply_debuff_to_target(self, debuff, current_time, stacks_to_apply=1, max_stacks=1):
        if debuff.name in self.target_active_debuffs:
            self.target_active_debuffs[debuff.name].append(debuff)
        else:
            self.target_active_debuffs[debuff.name] = [debuff]
        debuff.apply_effect(self, current_time)
        
        debuff.times_applied += 1
        
    def reset_state(self):
        super().reset_state()
        self.damage_taken = 0
        self.target_active_debuffs = {}