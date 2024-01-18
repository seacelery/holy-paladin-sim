from ..utils.misc_functions import format_time, update_target_buff_data

class Target:
    
    def __init__(self, name):
        self.name = name
        self.healing_received = 0
        self.target_active_buffs = {}
        self.healing_taken_modifier = 1
        
    def receive_heal(self, amount):
        self.healing_received += amount
        
    def apply_buff_to_target(self, buff, current_time, stacks_to_apply=1, max_stacks=1, caster=None):
        if buff.name in self.target_active_buffs:
            self.target_active_buffs[buff.name].append(buff)
        else:
            self.target_active_buffs[buff.name] = [buff]
        buff.apply_effect(self)
        
        buff.times_applied += 1
        update_target_buff_data(caster.target_buff_breakdown, buff.name, current_time, "applied", self.name, buff.duration, buff.current_stacks)
           
    # def refresh_buff_on_target(self, buff, caster, current_time):
    #     if buff.name in self.target_active_buffs:
    #         self.target_active_buffs[buff.name].duration = self.target_active_buffs[buff.name].base_duration
   
    def reset_state(self):
        self.healing_received = 0
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
        debuff.apply_effect(self)
        
        debuff.times_applied += 1
        
    def reset_state(self):
        super().reset_state()
        self.damage_taken = 0
        self.target_active_debuffs = {}