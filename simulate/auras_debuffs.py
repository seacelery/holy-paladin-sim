from auras import Debuff
from misc_functions import append_spell_heal_event, format_time, append_aura_stacks_decremented, append_aura_removed_event
from spells_passives import JudgmentOfLightSpell, GreaterJudgmentSpell
import random

# target debuffs


class JudgmentOfLightDebuff(Debuff):
    
    def __init__(self):
        super().__init__("Judgment of Light", 30, base_duration=30, current_stacks=5, max_stacks=5)
    
    def consume_stacks(self, caster, damage_targets, healing_targets, current_time):
        judgment_of_light_target = damage_targets
        
        # heal instantly for each stack
        for _ in range(self.current_stacks):          
            heal_value, is_crit = JudgmentOfLightSpell(caster).calculate_heal(caster)
            healing_target = random.choice(healing_targets)
            healing_target.receive_heal(heal_value)
            append_spell_heal_event(caster.events, self.name, caster, healing_target, heal_value, current_time, is_crit)
            
            self.current_stacks -= 1
            append_aura_stacks_decremented(caster.events, self.name, caster, current_time, self.current_stacks, target=judgment_of_light_target, duration=self.duration)
            
            # delete this if something bad happens
            current_time += 0.01
            
        if self.current_stacks == 0:
            del judgment_of_light_target.target_active_debuffs[self.name]
            append_aura_removed_event(caster.events, self.name, caster, judgment_of_light_target, current_time)
            
            
class GreaterJudgmentDebuff(Debuff):
    
    def __init__(self):
        super().__init__("Greater Judgment", 15)
        
    def consume_greater_judgment(self, caster, damage_targets, healing_targets, current_time):
        greater_judgment_target = damage_targets
        greater_judgment_spell = GreaterJudgmentSpell(caster)
        
        # infusion of light increases the healing by 150%, only 100% without inflo - add this
        if "Infusion of Light" in caster.active_auras:
            greater_judgment_spell.spell_healing_modifier = 2.5
            caster.remove_or_decrement_buff_on_self(caster.active_auras["Infusion of Light"], current_time)
        else:
            greater_judgment_spell.spell_healing_modifier = 1
        
        # greater judgment is not affected by mastery
        original_mastery_multiplier = caster.mastery_multiplier
        caster.mastery_multiplier = 1
        
        heal_value, is_crit = greater_judgment_spell.calculate_heal(caster)
        
        healing_target = random.choice(healing_targets)
        healing_target.receive_heal(heal_value)
        append_spell_heal_event(caster.events, self.name, caster, healing_target, heal_value, current_time, is_crit, is_absorb=greater_judgment_spell.is_absorb)
        
        del greater_judgment_target.target_active_debuffs[self.name]
        append_aura_removed_event(caster.events, self.name, caster, greater_judgment_target, current_time)
        
        # reset mastery to normal
        caster.mastery_multiplier = original_mastery_multiplier
    