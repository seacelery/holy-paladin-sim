import random

from .auras import Debuff
from ..utils.misc_functions import append_spell_heal_event, format_time, append_aura_stacks_decremented, append_aura_removed_event, update_spell_data_heals
from .spells_passives import JudgmentOfLightSpell, GreaterJudgmentSpell

# target debuffs


class JudgmentOfLightDebuff(Debuff):
    
    def __init__(self):
        super().__init__("Judgment of Light", 30, base_duration=30, current_stacks=5, max_stacks=5)
    
    def consume_stacks(self, caster, damage_targets, healing_targets, current_time):
        judgment_of_light_target = damage_targets
        total_judgment_of_light_healing = 0
        
        # heal instantly for each stack
        for _ in range(self.current_stacks):          
            heal_value, is_crit = JudgmentOfLightSpell(caster).calculate_heal(caster)
            healing_target = random.choice(healing_targets)
            healing_target.receive_heal(heal_value, caster)
            total_judgment_of_light_healing += heal_value
            
            update_spell_data_heals(caster.ability_breakdown, "Judgment of Light", healing_target, heal_value, is_crit)
            append_spell_heal_event(caster.events, self.name, caster, healing_target, heal_value, current_time, is_crit)
            
            self.current_stacks -= 1
            append_aura_stacks_decremented(caster.events, self.name, caster, current_time, self.current_stacks, target=judgment_of_light_target, duration=self.duration)
            
            # delete this if something bad happens
            current_time += 0.01
            
        if self.current_stacks == 0:
            del judgment_of_light_target.target_active_debuffs[self.name]
            append_aura_removed_event(caster.events, self.name, caster, judgment_of_light_target, current_time)
            
        return total_judgment_of_light_healing
            
            
class GreaterJudgmentDebuff(Debuff):
    
    def __init__(self):
        super().__init__("Greater Judgment", 15, base_duration=15)
        
    def consume_greater_judgment(self, caster, damage_targets, healing_targets, current_time):
        greater_judgment_target = damage_targets
        greater_judgment_spell = GreaterJudgmentSpell(caster)
        
        if "Infusion of Light" in caster.active_auras and caster.is_talent_active("Inflorescence of the Sunwell"):
            greater_judgment_spell.spell_healing_modifier = 2.5
        elif "Infusion of Light" in caster.active_auras:
            greater_judgment_spell.spell_healing_modifier = 2
        else:
            greater_judgment_spell.spell_healing_modifier = 1
        
        # greater judgment is not affected by mastery
        original_mastery_multiplier = caster.mastery_multiplier
        caster.mastery_multiplier = 1
        
        heal_value, is_crit = greater_judgment_spell.calculate_heal(caster)
        
        healing_target = random.choice(healing_targets)
        healing_target.receive_heal(heal_value, caster)
        
        update_spell_data_heals(caster.ability_breakdown, "Greater Judgment", healing_target, heal_value, is_crit)
        append_spell_heal_event(caster.events, self.name, caster, healing_target, heal_value, current_time, is_crit, is_absorb=greater_judgment_spell.is_absorb)
        
        del greater_judgment_target.target_active_debuffs[self.name]
        append_aura_removed_event(caster.events, self.name, caster, greater_judgment_target, current_time)
        
        # reset mastery to normal
        caster.mastery_multiplier = original_mastery_multiplier
        
        return heal_value
    