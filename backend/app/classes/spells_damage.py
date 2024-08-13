import random

from .spells import Spell
from .spells_healing import HammerAndAnvilHeal, TruthPrevailsHeal
from ..utils.misc_functions import format_time, increment_holy_power, append_aura_applied_event, append_aura_removed_event, append_aura_stacks_decremented, append_spell_heal_event, update_spell_data_heals, update_self_buff_data, update_mana_gained, add_talent_healing_multipliers
from .auras_debuffs import JudgmentOfLightDebuff, GreaterJudgmentDebuff
from .auras_buffs import BlessingOfDawn, AvengingWrathAwakening, AvengingCrusaderAwakening, EmpyreanLegacy, Veneration
from .summons import ConsecrationSummon, RighteousJudgmentSummon


class Judgment(Spell):
    
    SPELL_POWER_COEFFICIENT = 1.125 / 1.04
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
        
        # truth prevails
        if caster.is_talent_active("Truth Prevails"):
            self.MANA_COST *= 0.7
            self.mana_cost *= 0.7
        
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            self.bonus_crit = Judgment.BONUS_CRIT
        
        # justification
        if caster.is_talent_active("Justification"):
            self.spell_damage_modifier = 1.1
            
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):        
        # awakening
        if caster.is_talent_active("Awakening"):
            if "Awakening Ready" in caster.active_auras:
                # add 30% damage buff and guaranteed crit
                self.bonus_crit = 1
                self.spell_damage_modifier *= 1.4
        
        # avenging crusader        
        if caster.is_talent_active("Avenging Crusader") and "Avenging Crusader" in caster.active_auras:
            self.spell_damage_modifier *= 1.3
           
        cast_success, spell_crit, spell_damage = super().cast_damage_spell(caster, targets, current_time)
        
        judgment_of_light_healing = 0
        greater_judgment_healing = 0
        avenging_crusader_healing = 0
        if cast_success: 
            increment_holy_power(self, caster, current_time)
            target = targets[0]
            
            # liberation
            if caster.is_talent_active("Liberation") and "Liberation" in caster.active_auras and "Innervate" not in caster.active_auras:
                caster.active_auras["Liberation"].remove_effect(caster)
                del caster.active_auras["Liberation"]
                update_self_buff_data(caster.self_buff_breakdown, "Liberation", current_time, "expired")
            
            # veneration
            if caster.is_talent_active("Veneration"):
                if spell_crit:
                    if caster.is_talent_active("Vanguard's Momentum"):
                        if caster.abilities["Hammer of Wrath"].current_charges < caster.abilities["Hammer of Wrath"].max_charges:
                            caster.abilities["Hammer of Wrath"].current_charges += 1
                        else:
                            caster.abilities["Hammer of Wrath"].remaining_cooldown = 0
                    else:
                        caster.abilities["Hammer of Wrath"].remaining_cooldown = 0
                    caster.apply_buff_to_self(Veneration(), current_time) 
            
            # divine revelations
            if caster.is_talent_active("Divine Revelations"):
                if "Infusion of Light" in caster.active_auras:
                    divine_revelations_mana_gain = caster.max_mana * 0.005
                    caster.mana += divine_revelations_mana_gain
                    update_mana_gained(caster.ability_breakdown, "Divine Revelations (Judgment)", divine_revelations_mana_gain)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras:
                fading_light_absorb = spell_damage * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
        
            # awakening
            if caster.is_talent_active("Awakening"):
                if "Awakening Ready" in caster.active_auras:
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras:
                        caster.awakening_queued = True
                    else:
                        if caster.is_talent_active("Avenging Crusader"):
                            buff = AvengingCrusaderAwakening()
                        else:
                            buff = AvengingWrathAwakening()
                        caster.apply_buff_to_self(buff, current_time)
                        
                    del caster.active_auras["Awakening Ready"]
                        
                    update_self_buff_data(caster.self_buff_breakdown, "Awakening Ready", current_time, "expired")
             
                    append_aura_removed_event(caster.events, "Awakening Ready", caster, caster, current_time)
                    
                    # remove 30% damage buff
                    self.spell_damage_modifier /= 1.4
                    self.bonus_crit = 0
                    
            # avenging crusader        
            if caster.is_talent_active("Avenging Crusader") and "Avenging Crusader" in caster.active_auras:
                avenging_crusader_healing = spell_damage * 4.2 / 5
                for avenging_crusader_target in random.sample(caster.potential_healing_targets, 5):
                    avenging_crusader_target.receive_heal(avenging_crusader_healing, caster)
                    
                    update_spell_data_heals(caster.ability_breakdown, "Avenging Crusader (Judgment)", avenging_crusader_target, avenging_crusader_healing, spell_crit)
                    caster.handle_beacon_healing("Avenging Crusader (Judgment)", avenging_crusader_target, avenging_crusader_healing, current_time)
                
                self.spell_damage_modifier /= 1.3
            
            # empyrean legacy                  
            if caster.is_talent_active("Empyrean Legacy") and "Empyrean Legacy Cooldown" not in caster.active_auras:
                caster.apply_buff_to_self(EmpyreanLegacy(), current_time)    
            
            # greater judgment, add talent condition
            if caster.is_talent_active("Greater Judgment"):
                greater_judgment_debuff = GreaterJudgmentDebuff()
                target.apply_debuff_to_target(greater_judgment_debuff, current_time)
                append_aura_applied_event(caster.events, "Greater Judgment", caster, target, current_time)
                greater_judgment_healing = greater_judgment_debuff.consume_greater_judgment(caster, target, healing_targets, current_time)
            
            # judgment of light
            if caster.is_talent_active("Judgment of Light"):
                judgment_of_light_debuff = JudgmentOfLightDebuff()
                target.apply_debuff_to_target(judgment_of_light_debuff, current_time, stacks_to_apply=5, max_stacks=5)
                append_aura_applied_event(caster.events, "Judgment of Light", caster, target, current_time, current_stacks=5, max_stacks=5)
                judgment_of_light_healing = judgment_of_light_debuff.consume_stacks(caster, target, healing_targets, current_time)
                
            # righteous judgment
            if caster.is_talent_active("Righteous Judgment"):
                random_num = random.random()
                if random_num <= 0.5:
                    caster.apply_summon(RighteousJudgmentSummon(caster), current_time)
                
            # decrement stacks or remove infusion of light
            if "Infusion of Light" in caster.active_auras:
                # imbued infusions
                if caster.is_talent_active("Imbued Infusions"):
                    caster.abilities["Holy Shock"].remaining_cooldown -= 1
                    
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
                    
                if caster.is_talent_active("Valiance"):
                    # extended version (removed for now)
                    # holy_bulwark_targets = [target for target in caster.potential_healing_targets if "Holy Bulwark" in target.target_active_buffs]
                    # sacred_weapon_targets = [target for target in caster.potential_healing_targets if "Sacred Weapon" in target.target_active_buffs]
                    
                    # if len(holy_bulwark_targets) > 0:
                    #     for target in holy_bulwark_targets:
                    #         target.target_active_buffs["Holy Bulwark"][0].duration += 3
                    #     caster.active_auras["Holy Bulwark"].duration += 3
                    # if len(sacred_weapon_targets) > 0:
                    #     for target in sacred_weapon_targets:
                    #         target.target_active_buffs["Sacred Weapon"][0].duration += 3
                    #     caster.active_auras["Sacred Weapon"].duration += 3
                    # if len(holy_bulwark_targets) == 0 and len(sacred_weapon_targets) == 0:
                    
                    if "Holy Bulwark" in caster.abilities:
                        caster.abilities["Holy Bulwark"].remaining_cooldown -= 3
                    if "Sacred Weapon" in caster.abilities:
                        caster.abilities["Sacred Weapon"].remaining_cooldown -= 3
            
            # hammer and anvil               
            if caster.is_talent_active("Hammer and Anvil") and spell_crit:         
                hammer_and_anvil_heal, hammer_and_anvil_crit = HammerAndAnvilHeal(caster).calculate_heal(caster)
                hammer_and_anvil_heal = (1.5 * caster.spell_power * caster.versatility_multiplier) + (1.5 * caster.spell_power * 1.04)
                
                if hammer_and_anvil_crit:
                    hammer_and_anvil_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
                    
                hammer_and_anvil_target_count = 5
                hammer_and_anvil_heal = add_talent_healing_multipliers(hammer_and_anvil_heal, caster)
                
                chosen_targets = random.sample(caster.potential_healing_targets, hammer_and_anvil_target_count)
                for target in chosen_targets:
                    target.receive_heal(hammer_and_anvil_heal, caster)
                    update_spell_data_heals(caster.ability_breakdown, "Hammer and Anvil", target, hammer_and_anvil_heal, hammer_and_anvil_crit)
                    
            # truth prevails
            if caster.is_talent_active("Truth Prevails"):
                truth_prevails_heal, truth_prevails_crit = TruthPrevailsHeal(caster).calculate_heal(caster)
                caster.receive_self_heal(truth_prevails_heal)
                
                update_spell_data_heals(caster.ability_breakdown, "Truth Prevails", caster, truth_prevails_heal, truth_prevails_crit)
                
        return cast_success, spell_crit, spell_damage, judgment_of_light_healing, greater_judgment_healing, avenging_crusader_healing
           
            
class CrusaderStrike(Spell):
    
    # uses attack power instead of spell power
    SPELL_POWER_COEFFICIENT = 1.071 * 1.04 * 1.58
    BASE_COOLDOWN = 7.75
    MANA_COST = 0.006
    HOLY_POWER_GAIN = 1
    
    def __init__(self, caster):
        super().__init__("Crusader Strike", mana_cost=CrusaderStrike.MANA_COST, cooldown=CrusaderStrike.BASE_COOLDOWN, holy_power_gain=CrusaderStrike.HOLY_POWER_GAIN, hasted_cooldown=True) 
        self.is_damage_spell = True
        
        # holy infusion (removed)
        # if caster.is_talent_active("Holy Infusion"):
        #     self.holy_power_gain = 2
        #     self.spell_damage_modifier = 1.5
        
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):  
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_damage_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
            
        # avenging crusader        
        if caster.is_talent_active("Avenging Crusader"):
            self.spell_damage_modifier *= 1.3
            
        if "Avenging Crusader" in caster.active_auras:
            if self.max_charges == 1:
                self.max_charges = 2
                if self.current_charges < self.max_charges:
                    self.current_charges += 1
        else:
            self.max_charges = 1
            
        # blessed assurance
        if caster.is_talent_active("Blessed Assurance") and "Blessed Assurance" in caster.active_auras:
            self.spell_damage_modifier *= 1.2
        
        cast_success, spell_crit, spell_damage = super().cast_damage_spell(caster, targets, current_time)
        
        avenging_crusader_healing = 0
        crusaders_reprieve_heal = 0
        if cast_success:
            # reset reclamation
            if caster.is_talent_active("Reclamation"):
                self.spell_damage_modifier /= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
                caster.events.append(f"{format_time(current_time)}: {round(self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1), 2)} mana restored by Reclamation ({self.name})")
                reclamation_mana = self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1)
                caster.mana += reclamation_mana
                update_mana_gained(caster.ability_breakdown, "Reclamation (Crusader Strike)", reclamation_mana)
                
            # avenging crusader        
            if caster.is_talent_active("Avenging Crusader"):
                avenging_crusader_healing = spell_damage * 4.2 / 5
                for avenging_crusader_target in random.sample(caster.potential_healing_targets, 5):
                    avenging_crusader_target.receive_heal(avenging_crusader_healing, caster)
                    
                    update_spell_data_heals(caster.ability_breakdown, "Avenging Crusader (Crusader Strike)", avenging_crusader_target, avenging_crusader_healing, spell_crit)
                    caster.handle_beacon_healing("Avenging Crusader (Crusader Strike)", avenging_crusader_target, avenging_crusader_healing, current_time)
                
                self.spell_damage_modifier /= 1.3
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras:
                fading_light_absorb = spell_damage * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            increment_holy_power(self, caster, current_time)
            
            # crusader's reprieve is not affected by stats except health
            if caster.is_talent_active("Crusader's Reprieve"):
                crusaders_reprieve_heal = caster.max_health * 0.02
                caster.receive_self_heal(crusaders_reprieve_heal)
                
                update_spell_data_heals(caster.ability_breakdown, "Crusader's Reprieve", caster, crusaders_reprieve_heal, False)
                append_spell_heal_event(caster.events, "Crusader's Reprieve", caster, caster, crusaders_reprieve_heal, current_time, is_crit=False)
               
            # crusader's might 
            if caster.is_talent_active("Crusader's Might"):
                caster.abilities["Holy Shock"].remaining_cooldown -= 2
                caster.abilities["Judgment"].remaining_cooldown -= 2
                    
                if caster.abilities["Holy Shock"].remaining_cooldown <= 0 and caster.is_talent_active("Light's Conviction"):
                    caster.holy_shock_cooldown_overflow = abs(caster.abilities["Holy Shock"].remaining_cooldown)
                    caster.abilities["Holy Shock"].remaining_cooldown = max(caster.abilities["Holy Shock"].calculate_cooldown(caster) - caster.holy_shock_cooldown_overflow, 0)
                    if caster.abilities["Holy Shock"].current_charges < caster.abilities["Holy Shock"].max_charges:
                        caster.abilities["Holy Shock"].current_charges += 1
                        
            # blessed assurance
            if caster.is_talent_active("Blessed Assurance") and "Blessed Assurance" in caster.active_auras:
                self.spell_damage_modifier /= 1.2
                del caster.active_auras["Blessed Assurance"]                 
                update_self_buff_data(caster.self_buff_breakdown, "Blessed Assurance", current_time, "expired")
                
        return cast_success, spell_crit, spell_damage, crusaders_reprieve_heal, avenging_crusader_healing
    

class HammerOfWrath(Spell):
    
    # uses attack power instead of spell power
    SPELL_POWER_COEFFICIENT = 1.302 * 1.04 * 1.7625
    BASE_COOLDOWN = 7.5
    MANA_COST = 0.006
    CHARGES = 1
    HOLY_POWER_GAIN = 1
    
    def __init__(self, caster):
        super().__init__("Hammer of Wrath", mana_cost=HammerOfWrath.MANA_COST, cooldown=HammerOfWrath.BASE_COOLDOWN, holy_power_gain=HammerOfWrath.HOLY_POWER_GAIN, max_charges=HammerOfWrath.CHARGES, hasted_cooldown=True) 
        self.is_damage_spell = True
        
        # vanguard's momentum
        if caster.is_talent_active("Vanguard's Momentum"):
            self.max_charges = 2
            self.current_charges = self.max_charges
        
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):          
        cast_success, spell_crit, spell_damage = super().cast_damage_spell(caster, targets, current_time)
        veneration_healing = 0
        if cast_success:
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras:
                fading_light_absorb = spell_damage * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            # vanguard's momentum
            if caster.is_talent_active("Vanguard's Momentum") and caster.is_enemy_below_20_percent:
                self.holy_power_gain = 2
            else:
                self.holy_power_gain = 1
            
            increment_holy_power(self, caster, current_time)
            
            if caster.is_talent_active("Veneration"):
                targets = random.sample(caster.potential_healing_targets, 5)
                
                veneration_healing_per_target = spell_damage * 2 / len(targets)
                
                for target in targets:                   
                    if "Close to Heart" in caster.active_auras:
                        veneration_healing_per_target *= 1.04
                        
                    if "Aura Mastery" in caster.active_auras and caster.is_talent_active("Protection of Tyr"):
                        veneration_healing_per_target *= 1.1
                    
                    target.receive_heal(veneration_healing_per_target, caster)
                    update_spell_data_heals(caster.ability_breakdown, "Veneration", target, veneration_healing_per_target, spell_crit)
                    
                    caster.handle_beacon_healing("Veneration", target, veneration_healing_per_target, current_time)
                    
                if "Veneration" in caster.active_auras:
                    del caster.active_auras["Veneration"]
                    update_self_buff_data(caster.self_buff_breakdown, "Veneration", current_time, "expired")
                
        return cast_success, spell_crit, spell_damage, veneration_healing
    
    
class Consecration(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    BASE_COOLDOWN = 9
    
    def __init__(self, caster):
        super().__init__("Consecration", cooldown=Consecration.BASE_COOLDOWN, hasted_cooldown=True)
        self.is_damage_spell = True
        
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):
        cast_success, spell_crit, spell_damage = super().cast_damage_spell(caster, targets, current_time)
        if cast_success:
            caster.apply_summon(ConsecrationSummon(), current_time)
            
            if "Divine Guidance" in caster.active_auras:
                caster.active_auras["Divine Guidance"].remove_effect(caster)
                del caster.active_auras["Divine Guidance"]
                update_self_buff_data(caster.self_buff_breakdown, "Divine Guidance", current_time, "expired")