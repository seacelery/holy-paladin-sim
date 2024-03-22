import random
import copy

from .spells import Spell
from .auras_buffs import AvengingWrathBuff, DivineFavorBuff, InfusionOfLight, BlessingOfFreedomBuff, GlimmerOfLightBuff, DivineResonance, RisingSunlight, FirstLight, HolyReverberation, AwakeningStacks, AwakeningTrigger, DivinePurpose, BlessingOfDawn, BlessingOfDusk, RelentlessInquisitor, UnendingLight
from .spells_passives import GlimmerOfLightSpell
from .summons import LightsHammerSummon
from .target import BeaconOfLight
from ..utils.misc_functions import format_time, append_spell_heal_event, append_aura_applied_event, append_aura_removed_event, append_aura_stacks_decremented, increment_holy_power, calculate_beacon_healing, append_spell_beacon_event, update_spell_data_casts, update_spell_data_heals, update_spell_data_beacon_heals, update_spell_holy_power_gain, update_self_buff_data, update_target_buff_data, update_mana_gained

# KNOWN BUGS
# glimmer's stacking 4% healing skips the first glimmer so 0% at 1 glimmer -> 8% at 2 glimmers

def handle_glimmer_removal(caster, glimmer_targets, current_time, max_glimmer_targets):
    if len(glimmer_targets) > max_glimmer_targets:             
        oldest_active_glimmer = min(glimmer_targets, key=lambda glimmer_target: glimmer_target.target_active_buffs["Glimmer of Light"][0].duration)
        oldest_active_glimmer.apply_buff_to_target(HolyReverberation(caster), current_time, caster=caster)
        
        longest_reverberation_duration = max(buff_instance.duration for buff_instance in oldest_active_glimmer.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in oldest_active_glimmer.target_active_buffs and oldest_active_glimmer.target_active_buffs["Holy Reverberation"] else None
        if "Holy Reverberation" in oldest_active_glimmer.target_active_buffs:
            if len(oldest_active_glimmer.target_active_buffs["Holy Reverberation"]) > 0:
                caster.buff_events.append(f"{format_time(current_time)}: Holy Reverberation ({len(oldest_active_glimmer.target_active_buffs['Holy Reverberation'])}) applied to {oldest_active_glimmer.name}: {longest_reverberation_duration}s duration")
        
        append_aura_removed_event(caster.buff_events, "Glimmer of Light", caster, oldest_active_glimmer, current_time, oldest_active_glimmer.target_active_buffs["Glimmer of Light"][0].duration)
        del oldest_active_glimmer.target_active_buffs["Glimmer of Light"]
        
        update_target_buff_data(caster.target_buff_breakdown, "Glimmer of Light", current_time, "expired", oldest_active_glimmer.name)
        
        caster.glimmer_removal_counter += 1
        glimmer_targets.remove(oldest_active_glimmer)


# generators
class HolyShock(Spell):
    
    SPELL_ID = 20473
    SPELL_POWER_COEFFICIENT = 1.535 * 0.8
    MANA_COST = 0.028
    BASE_MANA_COST = 0.028
    BASE_COOLDOWN = 8.5
    HOLY_POWER_GAIN = 1
    CHARGES = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock", mana_cost=HolyShock.MANA_COST, base_mana_cost=HolyShock.BASE_MANA_COST, cooldown=HolyShock.BASE_COOLDOWN, holy_power_gain=HolyShock.HOLY_POWER_GAIN, max_charges=HolyShock.CHARGES, hasted_cooldown=True, is_heal=True)
        # light's conviction
        if caster.is_talent_active("Light's Conviction"):
            self.max_charges = 2
            self.current_charges = self.max_charges
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets):
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            self.bonus_crit = HolyShock.BONUS_CRIT + 0.08
        else:
            self.bonus_crit = HolyShock.BONUS_CRIT
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.15
            
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            # reset reclamation
            if caster.is_talent_active("Reclamation"):
                self.spell_healing_modifier /= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
                caster.events.append(f"{format_time(current_time)}: {round(self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1), 2)} mana restored by Reclamation ({self.name})")
                reclamation_mana = self.get_base_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1)
                caster.mana += reclamation_mana
                update_mana_gained(caster.ability_breakdown, "Reclamation (Holy Shock)", reclamation_mana)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = (10 + len(glimmer_targets) * 1.5) / 100
                if random.random() <= holy_shock_reset_chance:
                    self.reset_cooldown(caster, current_time)
            
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.15
                if caster.is_talent_active("Boundless Salvation"):
                    if "Tyr's Deliverance (self)" in caster.active_auras:
                        if caster.tyrs_deliverance_extended_by <= 38:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 2)
                            caster.tyrs_deliverance_extended_by += 2
                        elif 38 < caster.tyrs_deliverance_extended_by < 40:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 40 - caster.tyrs_deliverance_extended_by)
                            caster.tyrs_deliverance_extended_by += 40 - caster.tyrs_deliverance_extended_by
            
            # if crits, apply Infusion of Light 
            if spell_crit:
                if caster.is_talent_active("Inflorescence of the Sunwell"):
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time, stacks_to_apply=2, max_stacks=2)
                else:
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time)
                
            # handle holy power gain and logging
            increment_holy_power(self, caster, current_time)
            update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
            # apply glimmer
            total_glimmer_healing = 0
            if caster.is_talent_active("Glimmer of Light"):
                for glimmer_target in glimmer_targets:
                    glimmer_heal, glimmer_crit = GlimmerOfLightSpell(caster).calculate_heal(caster)
                    if len(glimmer_targets) > 1:
                        glimmer_heal_value = glimmer_heal * (1 + (0.04 * len(glimmer_targets))) / len(glimmer_targets)
                    else:
                        glimmer_heal_value = glimmer_heal
                    
                    if caster.is_talent_active("Glorious Dawn"):
                        glimmer_heal_value *= 1.1
                    
                    total_glimmer_healing += glimmer_heal_value
                    
                    caster.total_glimmer_healing += glimmer_heal_value
                    caster.glimmer_hits += 1
                    
                    # see healing by target for each glimmer proc
                    # glimmer_healing.append(f"{glimmer_target.name}: {glimmer_heal_value}, {glimmer_crit}")
                    # print(glimmer_healing)
                    
                    glimmer_target.receive_heal(glimmer_heal_value, caster)
                    caster.healing_by_ability["Glimmer of Light"] = caster.healing_by_ability.get("Glimmer of Light", 0) + glimmer_heal_value
                    
                    update_spell_data_casts(caster.ability_breakdown, "Glimmer of Light")
                    update_spell_data_heals(caster.ability_breakdown, "Glimmer of Light", glimmer_target, glimmer_heal_value, glimmer_crit)
                    append_spell_heal_event(caster.events, "Glimmer of Light", caster, glimmer_target, glimmer_heal_value, current_time, glimmer_crit)
                    
                    # overflowing light
                    if caster.is_talent_active("Overflowing Light"):
                        overflowing_light_absorb_value = glimmer_heal_value * 0.3
                        glimmer_target.receive_heal(overflowing_light_absorb_value, caster)
                        caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                        
                        update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", glimmer_target, overflowing_light_absorb_value, False)
                        append_spell_heal_event(caster.events, "Overflowing Light", caster, glimmer_target, overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                    
                    # beacon of light
                    caster.handle_beacon_healing("Glimmer of Light", glimmer_target, glimmer_heal_value, current_time, spell_display_name="Glimmer of Light (Holy Shock)")
                    
                target = targets[0]
                if target in glimmer_targets:
                    append_aura_removed_event(caster.buff_events, "Glimmer of Light", caster, target, current_time)
                    del target.target_active_buffs["Glimmer of Light"]
                    update_target_buff_data(caster.target_buff_breakdown, "Glimmer of Light", current_time, "expired", target.name)
                    
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    glimmer_targets.append(targets[0])
                    self.apply_holy_reverberation(caster, target, current_time)
                    # append_aura_applied_event(caster.buff_events, "Holy Reverberation", caster, target, current_time, longest_reverberation_duration)
                else:
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    
                    glimmer_targets.append(targets[0])
                
                    if caster.is_talent_active("Illumination"):
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 8)
                    else:
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 3)
                        
            # rising sunlight  
            if caster.is_talent_active("Rising Sunlight"):
                if "Rising Sunlight" in caster.active_auras:
                    caster.delayed_casts.append((RisingSunlightHolyShock(caster), current_time + 0.3, target))
                    caster.delayed_casts.append((RisingSunlightHolyShock(caster), current_time + 0.6, target))
                    caster.rising_sunlight_timer = 0
                    if caster.active_auras["Rising Sunlight"].current_stacks > 1:
                        caster.active_auras["Rising Sunlight"].current_stacks -= 1
                        
                        update_self_buff_data(caster.self_buff_breakdown, "Rising Sunlight", current_time, "stacks_decremented", caster.active_auras['Rising Sunlight'].duration, caster.active_auras["Rising Sunlight"].current_stacks)
                        append_aura_stacks_decremented(caster.buff_events, "Rising Sunlight", caster, current_time, caster.active_auras["Rising Sunlight"].current_stacks, duration=caster.active_auras["Rising Sunlight"].duration)
                    else:
                        caster.active_auras["Rising Sunlight"].remove_effect(caster)
                        del caster.active_auras["Rising Sunlight"]
                        
                        update_self_buff_data(caster.self_buff_breakdown, "Rising Sunlight", current_time, "expired")
                        append_aura_removed_event(caster.buff_events, "Rising Sunlight", caster, caster, current_time)
                        
            return cast_success, spell_crit, heal_amount, total_glimmer_healing
            
            
class Daybreak(Spell):
    
    SPELL_ID = 414170
    BASE_COOLDOWN = 45
    
    def __init__(self, caster):
        super().__init__("Daybreak", cooldown=Daybreak.BASE_COOLDOWN)  
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        total_glimmer_healing = 0
        if cast_success:
            # caster.events.append(f"{current_time}: mana: {caster.mana}")
            # caster.events.append(f"{current_time}: Glimmers before daybreak: {glimmer_targets}")
            caster.events.append(f"{format_time(current_time)}: {caster.name} cast {self.name}")
            
            number_of_glimmers_removed = len(glimmer_targets)
            caster.glimmer_removal_counter += number_of_glimmers_removed
            daybreak_mana_gain = 2000 * number_of_glimmers_removed
            caster.mana += daybreak_mana_gain
            update_mana_gained(caster.ability_breakdown, "Daybreak", daybreak_mana_gain)
            
            # rising sunlight
            if caster.is_talent_active("Rising Sunlight"):
                caster.apply_buff_to_self(RisingSunlight(), current_time, stacks_to_apply=3, max_stacks=3)
            
            # tier season 3 4pc  
            caster.apply_buff_to_self(FirstLight(), current_time)
            
            # adjust for daybreak 200% glimmer healing
            for glimmer_target in glimmer_targets:
                glimmer_heal, glimmer_crit = GlimmerOfLightSpell(caster).calculate_heal(caster)
                if len(glimmer_targets) > 1:
                    glimmer_heal_value = 2 * glimmer_heal * (1 + (0.04 * len(glimmer_targets))) / number_of_glimmers_removed
                else:
                    glimmer_heal_value = 2 * glimmer_heal
                
                if caster.is_talent_active("Glorious Dawn"):
                    glimmer_heal_value *= 1.1
                    
                total_glimmer_healing += glimmer_heal_value
                
                caster.total_glimmer_healing += glimmer_heal_value
                caster.glimmer_hits += 1
                
                glimmer_target.receive_heal(glimmer_heal_value, caster)
                caster.healing_by_ability["Glimmer of Light"] = caster.healing_by_ability.get("Glimmer of Light", 0) + glimmer_heal_value
                
                update_spell_data_casts(caster.ability_breakdown, "Glimmer of Light (Daybreak)")
                update_spell_data_heals(caster.ability_breakdown, "Glimmer of Light (Daybreak)", glimmer_target, glimmer_heal_value, glimmer_crit)
                append_spell_heal_event(caster.events, "Glimmer of Light", caster, glimmer_target, glimmer_heal_value, current_time, glimmer_crit)
                
                # overflowing light
                if caster.is_talent_active("Overflowing Light"):
                    overflowing_light_absorb_value = glimmer_heal_value * 0.3
                    glimmer_target.receive_heal(overflowing_light_absorb_value, caster)
                    caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                    
                    update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", glimmer_target, overflowing_light_absorb_value, False)
                    append_spell_heal_event(caster.events, "Overflowing Light", caster, glimmer_target, overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                
                # beacon of light
                caster.handle_beacon_healing("Glimmer of Light", glimmer_target, glimmer_heal_value, current_time, spell_display_name="Glimmer of Light (Daybreak)")
            
            for target in glimmer_targets[:]:
                append_aura_removed_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                del target.target_active_buffs["Glimmer of Light"]
                update_target_buff_data(caster.target_buff_breakdown, "Glimmer of Light", current_time, "expired", target.name)
                glimmer_targets.remove(target)
                
                target.apply_buff_to_target(HolyReverberation(caster), current_time, caster=caster)
                
                longest_reverberation_duration = max(buff_instance.duration for buff_instance in target.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in target.target_active_buffs and target.target_active_buffs["Holy Reverberation"] else None
                if "Holy Reverberation" in target.target_active_buffs:
                    if len(target.target_active_buffs["Holy Reverberation"]) > 0:
                        caster.buff_events.append(f"{format_time(current_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
        
        return cast_success, spell_crit, heal_amount, total_glimmer_healing
            
               
class RisingSunlightHolyShock(Spell):
    
    SPELL_ID = 20473
    SPELL_POWER_COEFFICIENT = 1.535
    HOLY_POWER_GAIN = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock (Rising Sunlight)", base_mana_cost=HolyShock.BASE_MANA_COST, holy_power_gain=RisingSunlightHolyShock.HOLY_POWER_GAIN, is_heal=True, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets):
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            self.bonus_crit = HolyShock.BONUS_CRIT + 0.08
        else:
            self.bonus_crit = HolyShock.BONUS_CRIT
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.15
            
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            
            # reset reclamation
            if caster.is_talent_active("Reclamation"):
                self.spell_healing_modifier /= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
                caster.events.append(f"{format_time(current_time)}: {round(self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1), 2)} mana restored by Reclamation ({self.name})")
                reclamation_mana = self.get_base_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1)
                caster.mana += reclamation_mana
                update_mana_gained(caster.ability_breakdown, "Reclamation (Holy Shock)", reclamation_mana)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = (10 + len(glimmer_targets) * 1.5) / 100
                if random.random() <= holy_shock_reset_chance:
                    caster.abilities["Holy Shock"].reset_cooldown(caster, current_time)
            
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.15
                if caster.is_talent_active("Boundless Salvation"):
                    if "Tyr's Deliverance (self)" in caster.active_auras:
                        if caster.tyrs_deliverance_extended_by <= 38:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 2)
                            caster.tyrs_deliverance_extended_by += 2
                        elif 38 < caster.tyrs_deliverance_extended_by < 40:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 40 - caster.tyrs_deliverance_extended_by)
                            caster.tyrs_deliverance_extended_by += 40 - caster.tyrs_deliverance_extended_by
            
            # if crits, apply Infusion of Light 
            if spell_crit:
                if caster.is_talent_active("Inflorescence of the Sunwell"):
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time, stacks_to_apply=2, max_stacks=2)
                else:
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time)
                    
            # handle holy power gain and logging
            increment_holy_power(self, caster, current_time)
            update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
            # apply glimmer
            total_glimmer_healing = 0
            if caster.is_talent_active("Glimmer of Light"):
                for glimmer_target in glimmer_targets:
                    glimmer_heal, glimmer_crit = GlimmerOfLightSpell(caster).calculate_heal(caster)
                    if len(glimmer_targets) > 1:
                        glimmer_heal_value = glimmer_heal * (1 + (0.04 * len(glimmer_targets))) / len(glimmer_targets)
                    else:
                        glimmer_heal_value = glimmer_heal
                    
                    if caster.is_talent_active("Glorious Dawn"):
                        glimmer_heal_value *= 1.1
                        
                    total_glimmer_healing += glimmer_heal_value
                    
                    caster.total_glimmer_healing += glimmer_heal_value
                    caster.glimmer_hits += 1
                    
                    glimmer_target.receive_heal(glimmer_heal_value, caster)
                    caster.healing_by_ability["Glimmer of Light"] = caster.healing_by_ability.get("Glimmer of Light", 0) + glimmer_heal_value
                    
                    update_spell_data_casts(caster.ability_breakdown, "Glimmer of Light (Rising Sunlight)")
                    update_spell_data_heals(caster.ability_breakdown, "Glimmer of Light (Rising Sunlight)", glimmer_target, glimmer_heal_value, glimmer_crit)
                    append_spell_heal_event(caster.events, "Glimmer of Light", caster, glimmer_target, glimmer_heal_value, current_time, glimmer_crit)
                    
                    # overflowing light
                    if caster.is_talent_active("Overflowing Light"):
                        overflowing_light_absorb_value = glimmer_heal_value * 0.3
                        glimmer_target.receive_heal(overflowing_light_absorb_value, caster)
                        caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                        
                        update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", glimmer_target, overflowing_light_absorb_value, False)
                        append_spell_heal_event(caster.events, "Overflowing Light", caster, glimmer_target, overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                    
                    # beacon of light
                    caster.handle_beacon_healing("Glimmer of Light", glimmer_target, glimmer_heal_value, current_time, spell_display_name="Glimmer of Light (Rising Sunlight)")
                    
                target = targets[0]
                if target in glimmer_targets:
                    # caster.events.append(f"{current_time}: {glimmer_targets}")
                    append_aura_removed_event(caster.buff_events, "Glimmer of Light", caster, target, current_time)
                    del target.target_active_buffs["Glimmer of Light"]
                    update_target_buff_data(caster.target_buff_breakdown, "Glimmer of Light", current_time, "expired", target.name)
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    glimmer_targets.append(targets[0])
                    self.apply_holy_reverberation(caster, target, current_time)
                else:
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    
                    glimmer_targets.append(targets[0])
                
                    # illumination
                    if caster.is_talent_active("Illumination"):
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 8)
                    else:
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 3)
                        
        return cast_success, spell_crit, heal_amount, total_glimmer_healing
            
                    
class DivineToll(Spell):
    
    SPELL_ID = 375576
    MANA_COST = 0.03
    BASE_COOLDOWN = 60
    
    def __init__(self, caster):
        super().__init__("Divine Toll", mana_cost=DivineToll.MANA_COST, cooldown=DivineToll.BASE_COOLDOWN)
        # quickened invocation
        if caster.is_talent_active("Quickened Invocation"):
            self.cooldown = 45
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            original_gcd = caster.hasted_global_cooldown
            
            caster.events.append(f"{format_time(current_time)}: {caster.name} cast {self.name}")

            # each holy shock procs glimmer exactly once on its target
            # bugged to heal 6 targets instead of 5 (usually)
            for i in range(6):
                caster.global_cooldown = 0
                non_glimmer_targets = [glimmer_target for glimmer_target in caster.potential_healing_targets if "Glimmer of Light" not in glimmer_target.target_active_buffs]
                non_glimmer_non_beacon_targets = [t for t in non_glimmer_targets if t not in caster.beacon_targets] 
                target = [random.choice(non_glimmer_non_beacon_targets)]    
                DivineTollHolyShock(caster).cast_healing_spell(caster, target, current_time, is_heal=True, glimmer_targets=glimmer_targets)
            
            caster.global_cooldown = original_gcd
            
            # divine resonance
            if caster.is_talent_active("Divine Resonance"):
                caster.apply_buff_to_self(DivineResonance(), current_time)
                
        return cast_success, spell_crit, heal_amount   
  
  
class DivineTollHolyShock(Spell):
    
    SPELL_ID = 20473
    SPELL_POWER_COEFFICIENT = 1.535
    HOLY_POWER_GAIN = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock (Divine Toll)", base_mana_cost=HolyShock.BASE_MANA_COST, holy_power_gain=DivineTollHolyShock.HOLY_POWER_GAIN, base_mana_cost=HolyShock.BASE_MANA_COST, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets):
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            self.bonus_crit = HolyShock.BONUS_CRIT + 0.08
        else:
            self.bonus_crit = HolyShock.BONUS_CRIT
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20

        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.15
            
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
            
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        total_glimmer_healing = 0
        if cast_success:
            # reset reclamation
            if caster.is_talent_active("Reclamation"):
                self.spell_healing_modifier /= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
                caster.events.append(f"{format_time(current_time)}: {round(self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1), 2)} mana restored by Reclamation ({self.name})")
                reclamation_mana = self.get_base_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1)
                caster.mana += reclamation_mana
                update_mana_gained(caster.ability_breakdown, "Reclamation (Holy Shock)", reclamation_mana)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = (10 + len(glimmer_targets) * 1.5) / 100
                if random.random() <= holy_shock_reset_chance:
                    caster.abilities["Holy Shock"].reset_cooldown(caster, current_time)
            
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.15
                if caster.is_talent_active("Boundless Salvation"):
                    if "Tyr's Deliverance (self)" in caster.active_auras:
                        if caster.tyrs_deliverance_extended_by <= 38:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 2)
                            caster.tyrs_deliverance_extended_by += 2
                        elif 38 < caster.tyrs_deliverance_extended_by < 40:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 40 - caster.tyrs_deliverance_extended_by)
                            caster.tyrs_deliverance_extended_by += 40 - caster.tyrs_deliverance_extended_by
            
            caster.divine_toll_holy_shock_count += 1
            
            # if crits, apply Infusion of Light 
            if spell_crit:
                if caster.is_talent_active("Inflorescence of the Sunwell"):
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time, stacks_to_apply=2, max_stacks=2)
                else:
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time)
                    
            # handle holy power gain and logging
            increment_holy_power(self, caster, current_time)
            update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
            # apply glimmers THEN calculate divine toll's glimmer healing  
            if caster.is_talent_active("Glimmer of Light"):       
                target = targets[0]
                if target in glimmer_targets:
                    append_aura_removed_event(caster.buff_events, "Glimmer of Light", caster, target, current_time)
                    del target.target_active_buffs["Glimmer of Light"]
                    update_target_buff_data(caster.target_buff_breakdown, "Glimmer of Light", current_time, "expired", target.name)
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    glimmer_targets.append(targets[0])
                    self.apply_holy_reverberation(caster, target, current_time)
                else:
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    
                    glimmer_targets.append(targets[0])
                
                    # illumination
                    if caster.is_talent_active("Illumination"):
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 8)
                    else:
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 3)
                    
                if caster.divine_toll_holy_shock_count == 5:
                    glimmer_heal, glimmer_crit = GlimmerOfLightSpell(caster).calculate_heal(caster)
                    if len(glimmer_targets) > 1:
                        glimmer_heal_value = glimmer_heal * (1 + (0.04 * len(glimmer_targets))) / len(glimmer_targets)
                    else:
                        glimmer_heal_value = glimmer_heal
                    
                    # glorious dawn    
                    if caster.is_talent_active("Glorious Dawn"):
                        glimmer_heal_value *= 1.1

                    total_glimmer_healing += glimmer_heal_value
                    
                    caster.total_glimmer_healing += glimmer_heal_value
                    caster.glimmer_hits += 1
                    
                    for target in glimmer_targets:    
                        target.receive_heal(glimmer_heal_value, caster)
                        caster.healing_by_ability["Glimmer of Light"] = caster.healing_by_ability.get("Glimmer of Light", 0) + glimmer_heal_value
                        append_spell_heal_event(caster.events, "Glimmer of Light", caster, target, glimmer_heal_value, current_time, glimmer_crit)
                        
                        update_spell_data_casts(caster.ability_breakdown, "Glimmer of Light (Divine Toll)")
                        update_spell_data_heals(caster.ability_breakdown, "Glimmer of Light (Divine Toll)", target, glimmer_heal_value, glimmer_crit)
                        
                        # overflowing light
                        if caster.is_talent_active("Overflowing Light"):
                            overflowing_light_absorb_value = glimmer_heal_value * 0.3
                            target.receive_heal(overflowing_light_absorb_value, caster)
                            caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                            
                            update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", target, overflowing_light_absorb_value, False)
                            append_spell_heal_event(caster.events, "Overflowing Light", caster, target, overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                        
                        # beacon of light 
                        caster.handle_beacon_healing("Glimmer of Light", target, glimmer_heal_value, current_time, spell_display_name="Glimmer of Light (Divine Toll)")
                                
                    caster.divine_toll_holy_shock_count = 0 
                    
        return cast_success, spell_crit, heal_amount, total_glimmer_healing
            
            
class DivineResonanceHolyShock(Spell):
    
    SPELL_ID = 20473
    SPELL_POWER_COEFFICIENT = 1.535
    HOLY_POWER_GAIN = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock (Divine Resonance)", base_mana_cost=HolyShock.BASE_MANA_COST, holy_power_gain=DivineTollHolyShock.HOLY_POWER_GAIN, is_heal=True, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets):
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            self.bonus_crit = HolyShock.BONUS_CRIT + 0.08
        else:
            self.bonus_crit = HolyShock.BONUS_CRIT
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.15
            
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
            
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            
            # reclamation
            if caster.is_talent_active("Reclamation"):
                self.spell_healing_modifier /= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
                caster.events.append(f"{format_time(current_time)}: {round(self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1), 2)} mana restored by Reclamation ({self.name})")
                reclamation_mana = self.get_base_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1)
                caster.mana += reclamation_mana
                update_mana_gained(caster.ability_breakdown, "Reclamation (Holy Shock)", reclamation_mana)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = (10 + len(glimmer_targets) * 1.5) / 100
                if random.random() <= holy_shock_reset_chance:
                    caster.abilities["Holy Shock"].reset_cooldown(caster, current_time)
            
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.15
                if caster.is_talent_active("Boundless Salvation"):
                    if "Tyr's Deliverance (self)" in caster.active_auras:
                        if caster.tyrs_deliverance_extended_by <= 38:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 2)
                            caster.tyrs_deliverance_extended_by += 2
                        elif 38 < caster.tyrs_deliverance_extended_by < 40:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 40 - caster.tyrs_deliverance_extended_by)
                            caster.tyrs_deliverance_extended_by += 40 - caster.tyrs_deliverance_extended_by
            
            # if crits, apply Infusion of Light 
            if spell_crit:
                if caster.is_talent_active("Inflorescence of the Sunwell"):
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time, stacks_to_apply=2, max_stacks=2)
                else:
                    caster.apply_buff_to_self(InfusionOfLight(caster), current_time)
            
            # handle holy power gain and logging
            increment_holy_power(self, caster, current_time)
            update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
            # glimmer of light
            if caster.is_talent_active("Glimmer of Light"):
                target = targets[0]
                if target in glimmer_targets:
                    append_aura_removed_event(caster.buff_events, "Glimmer of Light", caster, target, current_time)
                    del target.target_active_buffs["Glimmer of Light"]
                    update_target_buff_data(caster.target_buff_breakdown, "Glimmer of Light", current_time, "expired", target.name)
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    glimmer_targets.append(targets[0])
                    self.apply_holy_reverberation(caster, target, current_time)
                    # append_aura_applied_event(caster.buff_events, "Holy Reverberation", caster, target, current_time, longest_reverberation_duration)
                else:
                    target.apply_buff_to_target(GlimmerOfLightBuff(), current_time, caster=caster)
                    append_aura_applied_event(caster.buff_events, "Glimmer of Light", caster, target, current_time, target.target_active_buffs["Glimmer of Light"][0].duration)
                    caster.glimmer_application_counter += 1
                    
                    glimmer_targets.append(targets[0])
                
                    # illumination
                    if caster.is_talent_active("Illumination"):
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 8)
                    else:
                        handle_glimmer_removal(caster, glimmer_targets, current_time, 3)
                        
        return cast_success, spell_crit, heal_amount, 0


class HolyLight(Spell):
    
    SPELL_ID = 82326
    SPELL_POWER_COEFFICIENT = 5.096 * 0.8
    MANA_COST = 0.024
    HOLY_POWER_GAIN = 0
    BASE_CAST_TIME = 2.5
    
    def __init__(self, caster):
        super().__init__("Holy Light", base_mana_cost=HolyLight.MANA_COST, holy_power_gain=HolyLight.HOLY_POWER_GAIN, base_cast_time=HolyLight.BASE_CAST_TIME, is_heal=True)
        # tower of radiance
        if caster.is_talent_active("Tower of Radiance"):
            self.holy_power_gain = 1
    
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.15
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        resplendent_light_healing = 0
        if cast_success:
            # divine revelations
            if caster.is_talent_active("Divine Revelations"):
                if "Infusion of Light" in caster.active_auras:
                    divine_revelations_mana_gain = caster.max_mana * 0.005
                    caster.mana += divine_revelations_mana_gain
                    update_mana_gained(caster.ability_breakdown, "Divine Revelations (Holy Light)", divine_revelations_mana_gain)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
            
            # resplendent light
            if caster.is_talent_active("Resplendent Light"):
                resplendent_light_healing = heal_amount * 0.08
                target_pool = copy.deepcopy(caster.potential_healing_targets)
                for _ in range(5):
                    target = random.choice(target_pool)
                    target.receive_heal(resplendent_light_healing, caster)
                    target_pool.remove(target)
                    append_spell_heal_event(caster.events, "Resplendent Light", caster, target, resplendent_light_healing, current_time, is_crit=False) 
                    
                    update_spell_data_heals(caster.ability_breakdown, "Resplendent Light", target, resplendent_light_healing, False) 
                    
                    # beacon of light
                    caster.handle_beacon_healing("Resplendent Light", target, resplendent_light_healing, current_time)
        
                # add beacon healing here
            
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.15
                
                # boundless salvation
                if caster.is_talent_active("Boundless Salvation"):
                    if "Tyr's Deliverance (self)" in caster.active_auras:
                        if caster.tyrs_deliverance_extended_by <= 32:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 8)
                            caster.tyrs_deliverance_extended_by += 8
                        elif 32 < caster.tyrs_deliverance_extended_by < 40:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 40 - caster.tyrs_deliverance_extended_by)
                            caster.tyrs_deliverance_extended_by += 40 - caster.tyrs_deliverance_extended_by
            
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
                
                # handle inflorescence of the sunwell
                caster.infused_holy_light_count += 1

                if caster.infused_holy_light_count == 3:
                    self.holy_power_gain = 4
                    caster.infused_holy_light_count = 0
                else:
                    self.holy_power_gain = 3
                    
                increment_holy_power(self, caster, current_time)
                update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
                
                if caster.active_auras["Infusion of Light"].current_stacks > 1:
                    caster.active_auras["Infusion of Light"].current_stacks -= 1
                    append_aura_stacks_decremented(caster.events, "Infusion of Light", caster, current_time, caster.active_auras["Infusion of Light"].current_stacks, duration=caster.active_auras['Infusion of Light'].duration)
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Infusion of Light", current_time, "stacks_decremented", caster.active_auras['Infusion of Light'].duration, caster.active_auras["Infusion of Light"].current_stacks)
                else:
                    caster.active_auras["Infusion of Light"].remove_effect(caster)
                    del caster.active_auras["Infusion of Light"]
                    append_aura_removed_event(caster.events, "Infusion of Light", caster, caster, current_time)
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Infusion of Light", current_time, "expired")
            else:
                increment_holy_power(self, caster, current_time)
                update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
            # remove divine favor, start divine favor spell cd
            if "Divine Favor" in caster.active_auras:
                append_aura_removed_event(caster.events, "Divine Favor", caster, caster, current_time)
            
                caster.active_auras["Divine Favor"].remove_effect(caster)
                del caster.active_auras["Divine Favor"]
                caster.abilities["Divine Favor"].remaining_cooldown = 30
                
                update_self_buff_data(caster.self_buff_breakdown, "Divine Favor", current_time, "expired")
            
            # remove hand of divinity   
            if "Hand of Divinity" in caster.active_auras:        
                caster.remove_or_decrement_buff_on_self(caster.active_auras["Hand of Divinity"], current_time)
                
                update_self_buff_data(caster.self_buff_breakdown, "Hand of Divinity", current_time, "expired")
                
        return cast_success, spell_crit, heal_amount, resplendent_light_healing


class FlashOfLight(Spell):
    
    SPELL_ID = 19750
    SPELL_POWER_COEFFICIENT = 2.63 * 1.2
    MANA_COST = 0.036 
    BASE_MANA_COST = 0.036
    HOLY_POWER_GAIN = 0
    BASE_CAST_TIME = 1.5 
    
    def __init__(self, caster):
        super().__init__("Flash of Light", mana_cost=FlashOfLight.MANA_COST, base_mana_cost=FlashOfLight.BASE_MANA_COST, holy_power_gain=FlashOfLight.HOLY_POWER_GAIN, base_cast_time=FlashOfLight.BASE_CAST_TIME, is_heal=True)
        # tower of radiance
        if caster.is_talent_active("Tower of Radiance"):
            self.holy_power_gain = 1
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.15
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # divine revelations
        if caster.is_talent_active("Divine Revelations"):
            if "Infusion of Light" in caster.active_auras:
                self.spell_healing_modifier *= 1.2
            
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
            
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.15
                
                # boundless salvation
                if caster.is_talent_active("Boundless Salvation"):
                    if "Tyr's Deliverance (self)" in caster.active_auras:
                        if caster.tyrs_deliverance_extended_by <= 36:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 4)
                            caster.tyrs_deliverance_extended_by += 4
                        elif 36 < caster.tyrs_deliverance_extended_by < 40:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 40 - caster.tyrs_deliverance_extended_by)
                            caster.tyrs_deliverance_extended_by += 40 - caster.tyrs_deliverance_extended_by
            
            increment_holy_power(self, caster, current_time)
            update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
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

                # reset divine revelations
                if caster.is_talent_active("Divine Revelations"):
                    self.spell_healing_modifier /= 1.2
                
                if caster.active_auras["Infusion of Light"].current_stacks > 1:
                    caster.active_auras["Infusion of Light"].current_stacks -= 1
                    
                    append_aura_stacks_decremented(caster.events, "Infusion of Light", caster, current_time, caster.active_auras["Infusion of Light"].current_stacks, duration=caster.active_auras['Infusion of Light'].duration)
                    update_self_buff_data(caster.self_buff_breakdown, "Infusion of Light", current_time, "stacks_decremented", caster.active_auras['Infusion of Light'].duration, caster.active_auras["Infusion of Light"].current_stacks)
                else:
                    caster.active_auras["Infusion of Light"].remove_effect(caster)
                    del caster.active_auras["Infusion of Light"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Infusion of Light", current_time, "expired")
                    append_aura_removed_event(caster.events, "Infusion of Light", caster, caster, current_time)
                
            # remove divine favor, start divine favor spell cd
            if "Divine Favor" in caster.active_auras:
                append_aura_removed_event(caster.events, "Divine Favor", caster, caster, current_time)

                caster.active_auras["Divine Favor"].remove_effect(caster)
                del caster.active_auras["Divine Favor"]
                caster.abilities["Divine Favor"].remaining_cooldown = 30
                
                update_self_buff_data(caster.self_buff_breakdown, "Divine Favor", current_time, "expired")
                
        return cast_success, spell_crit, heal_amount
                
            
# spenders
class WordOfGlory(Spell):
    
    SPELL_ID = 85673
    SPELL_POWER_COEFFICIENT = 3.15 * 0.88
    MANA_COST = 0.012
    HOLY_POWER_COST = 3
    BASE_COOLDOWN = 0
    
    def __init__(self, caster):
        super().__init__("Word of Glory", mana_cost=WordOfGlory.MANA_COST, holy_power_cost=WordOfGlory.HOLY_POWER_COST, max_charges=0, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # divine purpose
        if caster.is_talent_active("Divine Purpose"): 
            if "Divine Purpose" in caster.active_auras:
                self.spell_healing_modifier *= 1.15
                self.holy_power_cost = 0
                self.mana_cost = 0
            
        # apply blessing of dawn healing (20% per stack without seal of order or fading light)
        if caster.is_talent_active("Of Dusk and Dawn"):
            if "Blessing of Dawn" in caster.active_auras:
                if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                    self.spell_healing_modifier *= 1.3
                elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                    self.spell_healing_modifier *= 1.6
        
        unending_light_modifier = 1           
        if caster.is_talent_active("Unending Light") and "Unending Light" in caster.active_auras:
            unending_light_modifier = 1 + (0.05 * caster.active_auras["Unending Light"].current_stacks)
            self.spell_healing_modifier *= unending_light_modifier
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        total_glimmer_healing = 0
        afterimage_heal = 0
        empyrean_legacy_light_of_dawn_healing = 0
        if cast_success:
            caster.holy_power -= self.holy_power_cost
            
            # reset healing modifier, remove blessing of dawn, and apply blessing of dusk
            if caster.is_talent_active("Of Dusk and Dawn"):
                if "Blessing of Dawn" in caster.active_auras:
                    if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                        self.spell_healing_modifier /= 1.3
                    elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                        self.spell_healing_modifier /= 1.6   
                    del caster.active_auras["Blessing of Dawn"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Blessing of Dawn", current_time, "expired")
                    append_aura_removed_event(caster.buff_events, "Blessing of Dawn", caster, caster, current_time)
                    caster.apply_buff_to_self(BlessingOfDusk(), current_time)
                    
            if caster.is_talent_active("Unending Light") and "Unending Light" in caster.active_auras:
                self.spell_healing_modifier /= unending_light_modifier
                
                del caster.active_auras["Unending Light"]     
                update_self_buff_data(caster.self_buff_breakdown, "Unending Light", current_time, "expired")
            
            # glistening radiance
            if caster.is_talent_active("Glistening Radiance") and caster.is_talent_active("Glimmer of Light"):
                glistening_radiance_chance = 0.25
                glimmer_targets = [target for target in caster.potential_healing_targets if "Glimmer of Light" in target.target_active_buffs]
                if len(glimmer_targets) > 0:
                    if random.random() <= glistening_radiance_chance:
                        spell = GlimmerOfLightSpell(caster)
                                
                        for glimmer_target in glimmer_targets:
                            glimmer_heal, glimmer_crit = spell.calculate_heal(caster)
                            if len(glimmer_targets) > 1:
                                glimmer_heal_value = glimmer_heal * (1 + (0.04 * len(glimmer_targets))) / len(glimmer_targets)
                            else:
                                glimmer_heal_value = glimmer_heal
                            
                            # glorious dawn
                            if caster.is_talent_active("Glorious Dawn"):
                                glimmer_heal_value *= 1.1
                                
                            total_glimmer_healing += glimmer_heal_value
                            
                            caster.total_glimmer_healing += glimmer_heal_value
                            caster.glimmer_hits += 1
                            
                            # see healing by target for each glimmer proc
                            # glimmer_healing.append(f"{glimmer_target.name}: {glimmer_heal_value}, {glimmer_crit}")
                            # print(glimmer_healing)
                            
                            glimmer_target.receive_heal(glimmer_heal_value, caster)
                            caster.healing_by_ability["Glimmer of Light"] = caster.healing_by_ability.get("Glimmer of Light", 0) + glimmer_heal_value
                            
                            update_spell_data_casts(caster.ability_breakdown, "Glimmer of Light (Glistening Radiance (Word of Glory))")
                            update_spell_data_heals(caster.ability_breakdown, "Glimmer of Light (Glistening Radiance (Word of Glory))", glimmer_target, glimmer_heal_value, glimmer_crit)
                            append_spell_heal_event(caster.events, "Glimmer of Light", caster, glimmer_target, glimmer_heal_value, current_time, glimmer_crit)
                            
                            # overflowing light
                            if caster.is_talent_active("Overflowing Light"):
                                overflowing_light_absorb_value = glimmer_heal_value * 0.3
                                glimmer_target.receive_heal(overflowing_light_absorb_value, caster)
                                caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                                
                                update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", glimmer_target, overflowing_light_absorb_value, False)
                                append_spell_heal_event(caster.events, "Overflowing Light", caster, glimmer_target, overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                            
                            # beacon of light
                            caster.handle_beacon_healing("Glimmer of Light", glimmer_target, glimmer_heal_value, current_time, spell_display_name="Glimmer of Light (Glistening Radiance)")

            # afterimage
            if caster.is_talent_active("Afterimage"):
                # process afterimage heal
                if "Divine Purpose" not in caster.active_auras:
                    caster.afterimage_counter += self.holy_power_cost
                    caster.events.append(f"{format_time(current_time)}: Afterimage ({caster.afterimage_counter})")
                    
                if caster.afterimage_counter >= 20:
                    caster.afterimage_counter = caster.afterimage_counter % 20
                    afterimage_heal, afterimage_crit = self.calculate_heal(caster)
                    afterimage_heal *= 0.3
                    
                    targets[0].receive_heal(afterimage_heal, caster)
                    
                    update_spell_data_heals(caster.ability_breakdown, "Afterimage", targets[0], afterimage_heal, afterimage_crit)
                    append_spell_heal_event(caster.events, "Afterimage", caster, targets[0], afterimage_heal, current_time, is_crit=False)
                    
                    # beacon of light
                    caster.handle_beacon_healing("Afterimage", targets[0], afterimage_heal, current_time)
            
            # divine purpose
            if caster.is_talent_active("Divine Purpose"):            
                if "Divine Purpose" in caster.active_auras:
                    del caster.active_auras["Divine Purpose"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Divine Purpose", current_time, "expired")
                    append_aura_removed_event(caster.events, "Divine Purpose", caster, caster, current_time)
                    self.spell_healing_modifier /= 1.15
                    self.holy_power_cost = 3
                    self.mana_cost = WordOfGlory.MANA_COST
                
                divine_purpose_chance = 0.15
                if random.random() <= divine_purpose_chance:
                    caster.apply_buff_to_self(DivinePurpose(), current_time)
            
            # awakening
            if caster.is_talent_active("Awakening"):
                if "Awakening" in caster.active_auras:
                    caster.apply_buff_to_self(caster.active_auras["Awakening"], current_time, stacks_to_apply=1, max_stacks=12)
                    if caster.active_auras["Awakening"].current_stacks >= 12:
                        del caster.active_auras["Awakening"]
                        
                        update_self_buff_data(caster.self_buff_breakdown, "Awakening", current_time, "expired")
                        append_aura_removed_event(caster.events, "Awakening", caster, caster, current_time)
                        caster.apply_buff_to_self(AwakeningTrigger(), current_time)
                        caster.awakening_trigger_times.update({round(current_time): 1})
                else:
                    caster.apply_buff_to_self(AwakeningStacks(), current_time, stacks_to_apply=1, max_stacks=12)
            
            # empyrean legacy        
            if caster.is_talent_active("Empyrean Legacy") and "Empyrean Legacy" in caster.active_auras:
                light_of_dawn = caster.abilities["Light of Dawn"]

                non_beacon_targets = [target for target in caster.potential_healing_targets if not isinstance(target, BeaconOfLight)]
                targets = caster.choose_multiple_targets(light_of_dawn, non_beacon_targets)
                
                for target in targets:
                    healing_value, is_crit = light_of_dawn.calculate_heal(caster)
                    healing_value *= 1.25
                    
                    target.receive_heal(healing_value, caster)
                    
                    update_spell_data_heals(caster.ability_breakdown, light_of_dawn.name, target, healing_value, is_crit)
                    caster.handle_beacon_healing(light_of_dawn.name, target, healing_value, current_time)
                    
                    empyrean_legacy_light_of_dawn_healing += healing_value
                    
                caster.remove_or_decrement_buff_on_self(caster.active_auras["Empyrean Legacy"], current_time)
            
            # relentless inquisitor    
            if caster.is_talent_active("Relentless Inquisitor"):
                caster.apply_buff_to_self(RelentlessInquisitor(), current_time, stacks_to_apply=1, max_stacks=5)
                    
        return cast_success, spell_crit, heal_amount, total_glimmer_healing, afterimage_heal, empyrean_legacy_light_of_dawn_healing
           
            
class LightOfDawn(Spell):
    
    SPELL_ID = 85222
    SPELL_POWER_COEFFICIENT = 0.8334 * 0.8
    MANA_COST = 0.012
    HOLY_POWER_COST = 3
    BASE_COOLDOWN = 0
    TARGET_COUNT = 5
    
    def __init__(self, caster):
        super().__init__("Light of Dawn", mana_cost=LightOfDawn.MANA_COST, holy_power_cost=LightOfDawn.HOLY_POWER_COST, healing_target_count=LightOfDawn.TARGET_COUNT, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # divine purpose
        if caster.is_talent_active("Divine Purpose"): 
            if "Divine Purpose" in caster.active_auras:
                self.spell_healing_modifier *= 1.15
                self.holy_power_cost = 0
                self.mana_cost = 0
                
        # apply blessing of dawn healing (20% per stack without seal of order or fading light)
        if caster.is_talent_active("Of Dusk and Dawn"):
            if "Blessing of Dawn" in caster.active_auras:
                if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                    self.spell_healing_modifier *= 1.3
                elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                    self.spell_healing_modifier *= 1.6
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        total_glimmer_healing = 0
        if cast_success:
            caster.holy_power -= self.holy_power_cost
            # unending light
            if "Unending Light" in caster.active_auras:
                caster.apply_buff_to_self(caster.active_auras["Unending Light"], current_time, stacks_to_apply=self.holy_power_cost, max_stacks=9)
            else:
                caster.apply_buff_to_self(UnendingLight(self.holy_power_cost), current_time, stacks_to_apply=self.holy_power_cost, max_stacks=9)
            
            # reset healing modifier, remove blessing of dawn, and apply blessing of dusk
            if caster.is_talent_active("Of Dusk and Dawn"):
                if "Blessing of Dawn" in caster.active_auras:
                    if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                        self.spell_healing_modifier /= 1.3
                    elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                        self.spell_healing_modifier /= 1.6   
                    del caster.active_auras["Blessing of Dawn"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Blessing of Dawn", current_time, "expired")
                    append_aura_removed_event(caster.buff_events, "Blessing of Dawn", caster, caster, current_time)
                    caster.apply_buff_to_self(BlessingOfDusk(), current_time)
            
            # glistening radiance
            if caster.is_talent_active("Glistening Radiance") and caster.is_talent_active("Glimmer of Light"):
                glistening_radiance_chance = 0.25
                glimmer_targets = [target for target in caster.potential_healing_targets if "Glimmer of Light" in target.target_active_buffs]
                if len(glimmer_targets) > 0:
                    if random.random() <= glistening_radiance_chance:
                        spell = GlimmerOfLightSpell(caster)
                                
                        for glimmer_target in glimmer_targets:
                            glimmer_heal, glimmer_crit = spell.calculate_heal(caster)
                            if len(glimmer_targets) > 1:
                                glimmer_heal_value = glimmer_heal * (1 + (0.04 * len(glimmer_targets))) / len(glimmer_targets)
                            else:
                                glimmer_heal_value = glimmer_heal
                            
                            # glorious dawn
                            if caster.is_talent_active("Glorious Dawn"):
                                glimmer_heal_value *= 1.1
                                
                            total_glimmer_healing += glimmer_heal_value
                            
                            caster.total_glimmer_healing += glimmer_heal_value
                            caster.glimmer_hits += 1
                            
                            # see healing by target for each glimmer proc
                            # glimmer_healing.append(f"{glimmer_target.name}: {glimmer_heal_value}, {glimmer_crit}")
                            # print(glimmer_healing)
                            
                            glimmer_target.receive_heal(glimmer_heal_value, caster)
                            caster.healing_by_ability["Glimmer of Light"] = caster.healing_by_ability.get("Glimmer of Light", 0) + glimmer_heal_value
                            
                            update_spell_data_casts(caster.ability_breakdown, "Glimmer of Light (Glistening Radiance (Light of Dawn))")
                            update_spell_data_heals(caster.ability_breakdown, "Glimmer of Light (Glistening Radiance (Light of Dawn))", glimmer_target, glimmer_heal_value, glimmer_crit)
                            append_spell_heal_event(caster.events, "Glimmer of Light", caster, glimmer_target, glimmer_heal_value, current_time, glimmer_crit)
                            
                            # overflowing light
                            if caster.is_talent_active("Overflowing Light"):
                                overflowing_light_absorb_value = glimmer_heal_value * 0.3
                                glimmer_target.receive_heal(overflowing_light_absorb_value, caster)
                                caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                                
                                update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", glimmer_target, overflowing_light_absorb_value, False)
                                append_spell_heal_event(caster.events, "Overflowing Light", caster, glimmer_target, overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                            
                            # beacon of light
                            caster.handle_beacon_healing("Glimmer of Light", glimmer_target, glimmer_heal_value, current_time, spell_display_name="Glimmer of Light (Glistening Radiance)")                   
            
            # afterimage
            if caster.is_talent_active("Afterimage"):
                if "Divine Purpose" not in caster.active_auras:
                    caster.afterimage_counter += self.holy_power_cost
                caster.events.append(f"{format_time(current_time)}: Afterimage ({caster.afterimage_counter})")
            
            # divine purpose
            if caster.is_talent_active("Divine Purpose"): 
                if "Divine Purpose" in caster.active_auras:
                    del caster.active_auras["Divine Purpose"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Divine Purpose", current_time, "expired")
                    append_aura_removed_event(caster.events, "Divine Purpose", caster, caster, current_time)
                    self.spell_healing_modifier /= 1.15
                    self.holy_power_cost = 3
                    self.mana_cost = LightOfDawn.MANA_COST
                
                divine_purpose_chance = 0.15
                if random.random() <= divine_purpose_chance:
                    caster.apply_buff_to_self(DivinePurpose(), current_time)
            
            # awakening
            if caster.is_talent_active("Awakening"):
                if "Awakening" in caster.active_auras:
                    caster.apply_buff_to_self(caster.active_auras["Awakening"], current_time, stacks_to_apply=1, max_stacks=12)
                    if caster.active_auras["Awakening"].current_stacks >= 12:
                        del caster.active_auras["Awakening"]
                        
                        update_self_buff_data(caster.self_buff_breakdown, "Awakening", current_time, "expired")
                        append_aura_removed_event(caster.events, "Awakening", caster, caster, current_time)
                        caster.apply_buff_to_self(AwakeningTrigger(), current_time)
                        caster.awakening_trigger_times.update({round(current_time): 1})
                else:
                    caster.apply_buff_to_self(AwakeningStacks(), current_time, stacks_to_apply=1, max_stacks=12)
            
            # relentless inquisitor        
            if caster.is_talent_active("Relentless Inquisitor"):
                if "Relentless Inquisitor" in caster.active_auras:
                    relentless_inquisitor = caster.active_auras["Relentless Inquisitor"]
                    
                    if relentless_inquisitor.current_stacks < relentless_inquisitor.max_stacks:
                        relentless_inquisitor.remove_effect(caster)
                        relentless_inquisitor.current_stacks += 1
                        relentless_inquisitor.apply_effect(caster)
                    
                    relentless_inquisitor.duration = relentless_inquisitor.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Relentless Inquisitor", current_time, "applied", relentless_inquisitor.duration, relentless_inquisitor.current_stacks)
                    
                else:
                    caster.apply_buff_to_self(RelentlessInquisitor(), current_time, stacks_to_apply=1, max_stacks=5)
                    
        return cast_success, spell_crit, heal_amount, total_glimmer_healing


class LightsHammerSpell(Spell):
    
    SPELL_ID = 114158
    BASE_COOLDOWN = 60
    MANA_COST = 0.036
    
    def __init__(self, caster):
        super().__init__("Light's Hammer", mana_cost=LightsHammerSpell.MANA_COST, cooldown=LightsHammerSpell.BASE_COOLDOWN)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_summon(LightsHammerSummon(), current_time)
                
                
class LightsHammerHeal(Spell):
    
    SPELL_ID = 114158
    SPELL_POWER_COEFFICIENT = 0.4 * 0.8
    TARGET_COUNT = 6
    
    def __init__(self, caster):
        super().__init__("Light's Hammer", healing_target_count=LightsHammerHeal.TARGET_COUNT, off_gcd=True)