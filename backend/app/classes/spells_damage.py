from .spells import Spell
from ..utils.misc_functions import format_time, increment_holy_power, append_aura_applied_event, append_aura_removed_event, append_aura_stacks_decremented, append_spell_heal_event, update_spell_data_heals, update_self_buff_data
from .auras_debuffs import JudgmentOfLightDebuff, GreaterJudgmentDebuff
from .auras_buffs import BlessingOfDawn
from .spells_auras import AvengingWrathBuff
from .target import Player

# DAMAGE SPELLS


class Judgment(Spell):
    
    SPELL_ID = 20271
    SPELL_POWER_COEFFICIENT = 0.610542 
    BASE_COOLDOWN = 12
    MANA_COST = 0.024
    HOLY_POWER_GAIN = 1
    BONUS_CRIT = 0.08
    
    def __init__(self, caster):
        # seal of alacrity cdr
        if caster.is_talent_active("Seal of Alacrity") and caster.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] == 1:
            self.BASE_COOLDOWN -= 0.5
        elif caster.is_talent_active("Seal of Alacrity") and caster.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] == 2:
            self.BASE_COOLDOWN -= 1
        
        super().__init__("Judgment", mana_cost=Judgment.MANA_COST, cooldown=self.BASE_COOLDOWN, holy_power_gain=Judgment.HOLY_POWER_GAIN, hasted_cooldown=True) 
        self.is_damage_spell = True
        
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            self.bonus_crit = Judgment.BONUS_CRIT
        
        # justification (10% judge damage talent)
        if caster.is_talent_active("Justification"):
            self.spell_damage_modifier = 1.1
            
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):
        if caster.is_talent_active("Awakening"):
            if "Awakening READY!!!!!!" in caster.active_auras:
                # add 30% damage buff and guaranteed crit
                self.bonus_crit = 1
                self.spell_damage_modifier *= 1.3
            
        cast_success, spell_crit = super().cast_damage_spell(caster, targets, current_time)
        if cast_success:
            
            increment_holy_power(self, caster)
            target = targets[0]
            
            # divine revelations
            if caster.is_talent_active("Divine Revelations"):
                if "Infusion of Light" in caster.active_auras:
                    caster.mana += caster.base_mana * 0.005
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
        
            # awakening
            if caster.is_talent_active("Awakening"):
                if "Awakening READY!!!!!!" in caster.active_auras:
                    buff = AvengingWrathBuff()
                    buff.duration = 12
                    
                    # remove 30% damage buff
                    self.spell_damage_modifier /= 1.3
                    self.bonus_crit = 0
                    
                    caster.apply_buff_to_self(buff, current_time)
                    del caster.active_auras["Awakening READY!!!!!!"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Awakening READY!!!!!!", current_time, "expired")
                    append_aura_removed_event(caster.events, "Awakening READY!!!!!!", caster, caster, current_time)
                
            # decrement stacks or remove infusion of light
            if "Infusion of Light" in caster.active_auras:
                # imbued infusions
                if caster.is_talent_active("Imbued Infusions"):
                    caster.abilities["Holy Shock"].remaining_cooldown -= 2
                    
                    if caster.abilities["Holy Shock"].remaining_cooldown <= 0 and caster.is_talent_active("Light's Conviction"):
                        caster.holy_shock_cooldown_overflow = abs(caster.abilities["Holy Shock"].remaining_cooldown)
                        caster.abilities["Holy Shock"].remaining_cooldown = max(caster.abilities["Holy Shock"].calculate_cooldown(caster) - caster.holy_shock_cooldown_overflow, 0)
                        if caster.abilities["Holy Shock"].current_charges < caster.abilities["Holy Shock"].max_charges:
                            caster.abilities["Holy Shock"].current_charges += 1
                
                if caster.active_auras["Infusion of Light"].current_stacks > 1:
                    caster.active_auras["Infusion of Light"].current_stacks -= 1
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Infusion of Light", current_time, "stacks_decremented", caster.active_auras['Infusion of Light'].duration, caster.active_auras["Infusion of Light"].current_stacks)
                    append_aura_stacks_decremented(caster.buff_events, "Infusion of Light", caster, current_time, caster.active_auras["Infusion of Light"].current_stacks, duration=caster.active_auras['Infusion of Light'].duration)
                else:
                    caster.active_auras["Infusion of Light"].remove_effect(caster)
                    del caster.active_auras["Infusion of Light"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Infusion of Light", current_time, "expired")
                    append_aura_removed_event(caster.buff_events, "Infusion of Light", caster, caster, current_time)

            # apply greater judgment, add talent condition
            if caster.is_talent_active("Greater Judgment"):
                greater_judgment_debuff = GreaterJudgmentDebuff()
                target.apply_debuff_to_target(greater_judgment_debuff, current_time)
                append_aura_applied_event(caster.events, "Greater Judgment", caster, target, current_time)
                greater_judgment_debuff.consume_greater_judgment(caster, target, healing_targets, current_time)
            
            # apply judgment of light, add talent condition
            if caster.is_talent_active("Judgment of Light"):
                judgment_of_light_debuff = JudgmentOfLightDebuff()
                target.apply_debuff_to_target(judgment_of_light_debuff, current_time, stacks_to_apply=5, max_stacks=5)
                append_aura_applied_event(caster.events, "Judgment of Light", caster, target, current_time, current_stacks=5, max_stacks=5)
                judgment_of_light_debuff.consume_stacks(caster, target, healing_targets, current_time)
           
            
class CrusaderStrike(Spell):
    
    # uses attack power not spell power
    SPELL_ID = 35395
    SPELL_POWER_COEFFICIENT = 1.071 * 1.04
    BASE_COOLDOWN = 7.75
    MANA_COST = 0.006
    HOLY_POWER_GAIN = 1
    
    def __init__(self, caster):
        super().__init__("Crusader Strike", mana_cost=CrusaderStrike.MANA_COST, cooldown=CrusaderStrike.BASE_COOLDOWN, holy_power_gain=CrusaderStrike.HOLY_POWER_GAIN, hasted_cooldown=True) 
        self.is_damage_spell = True
        
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):  
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_damage_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
        
        cast_success, spell_crit = super().cast_damage_spell(caster, targets, current_time)
        if cast_success:
            # reset reclamation
            if caster.is_talent_active("Reclamation"):
                self.spell_damage_modifier /= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
                caster.events.append(f"{format_time(current_time)}: {round(self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1), 2)} mana restored by Reclamation ({self.name})")
                caster.mana += self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
            
            increment_holy_power(self, caster)
            
            # crusader's reprieve is not affected by stats except health
            if caster.is_talent_active("Crusader's Reprieve"):
                crusaders_reprieve_heal = caster.max_health * 0.02
                caster.receive_self_heal(crusaders_reprieve_heal)
                
                update_spell_data_heals(caster.ability_breakdown, "Crusader's Reprieve", caster, crusaders_reprieve_heal, False)
                append_spell_heal_event(caster.events, "Crusader's Reprieve", caster, caster, crusaders_reprieve_heal, current_time, is_crit=False)

