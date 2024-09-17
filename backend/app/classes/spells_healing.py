import random
import copy

from .spells import Spell
from .auras_buffs import InfusionOfLight, GlimmerOfLightBuff, DivineResonance, RisingSunlight, FirstLight, HolyReverberation, AwakeningStacks, AwakeningTrigger, DivinePurpose, BlessingOfDawn, BlessingOfDusk, RelentlessInquisitor, UnendingLight, Veneration, UntemperedDedication, MaraadsDyingBreath, DawnlightAvailable, Dawnlight, EternalFlameBuff, GleamingRays, SunSear, SolarGrace, SunsAvatar, BlessedAssurance, DivineGuidance, DivineFavorBuff, PureLight, Liberation
from .spells_passives import GlimmerOfLightSpell
from .summons import LightsHammerSummon
from ..utils.misc_functions import format_time, append_spell_heal_event, append_aura_applied_event, append_aura_removed_event, append_aura_stacks_decremented, increment_holy_power, update_spell_data_casts, update_spell_data_heals, update_spell_holy_power_gain, update_self_buff_data, update_target_buff_data, update_mana_gained, handle_flat_cdr


def handle_glimmer_removal(caster, glimmer_targets, current_time, max_glimmer_targets):
    if len(glimmer_targets) > max_glimmer_targets:             
        oldest_active_glimmer = min(glimmer_targets, key=lambda glimmer_target: glimmer_target.target_active_buffs["Glimmer of Light"][0].duration)
        
        if caster.set_bonuses["dragonflight_season_3"] >= 2:
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
    
    SPELL_POWER_COEFFICIENT = 2.266
    MANA_COST = 0.026
    BASE_MANA_COST = 0.026
    BASE_COOLDOWN = 9.5
    HOLY_POWER_GAIN = 1
    CHARGES = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock", mana_cost=HolyShock.MANA_COST, base_mana_cost=HolyShock.BASE_MANA_COST, cooldown=HolyShock.BASE_COOLDOWN, holy_power_gain=HolyShock.HOLY_POWER_GAIN, max_charges=HolyShock.CHARGES, hasted_cooldown=True, is_heal=True)
            
        # tww season 1 tier 2pc  
        if caster.set_bonuses["tww_season_1"] >= 2:
            self.BASE_COOLDOWN /= 1.1
            self.cooldown /= 1.1
            
        # light's conviction
        if caster.is_talent_active("Light's Conviction"):
            self.max_charges = 2
            self.current_charges = self.max_charges
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets, initial_cast=True):
        bonus_crit = 0
        
        # tww season 1 tier 2pc
        if caster.set_bonuses["tww_season_1"] >= 2:
            self.spell_healing_modifier *= 1.1
        
        # blessing of an'she
        if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
            self.spell_healing_modifier *= 3
        
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            bonus_crit += 0.08      
             
        # luminosity    
        if caster.is_talent_active("Luminosity"):
            bonus_crit += 0.05
        
        self.bonus_crit = HolyShock.BONUS_CRIT + bonus_crit
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.12
            
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
        
        # light of the martyr & bestow light    
        if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
            cumulative_healing_mod = 1.2
            if caster.is_talent_active("Bestow Light") and "Bestow Light" in caster.active_auras:
                cumulative_healing_mod += 0.05 * caster.active_auras["Bestow Light"].current_stacks
            self.spell_healing_modifier *= cumulative_healing_mod
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal, exclude_cast=not initial_cast, initial_cast=initial_cast)
        barrier_of_faith_absorb = 0
        if cast_success:
            # tww season 1 tier 2pc
            if caster.set_bonuses["tww_season_1"] >= 2:
                self.spell_healing_modifier /= 1.1
            
            # blessing of an'she
            if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
                self.spell_healing_modifier /= 3
                del caster.active_auras["Blessing of An'she"]
                update_self_buff_data(caster.self_buff_breakdown, "Blessing of An'she", current_time, "expired")
                
            # sun sear
            if spell_crit and caster.is_talent_active("Sun Sear"):
                targets[0].apply_buff_to_target(SunSear(caster), current_time, caster=caster)
            
            # reset reclamation
            if caster.is_talent_active("Reclamation"):
                self.spell_healing_modifier /= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
                caster.events.append(f"{format_time(current_time)}: {round(self.get_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1), 2)} mana restored by Reclamation ({self.name})")
                reclamation_mana = self.get_base_mana_cost(caster) * ((1 - caster.average_raid_health_percentage) * 0.1)
                caster.mana += reclamation_mana
                update_mana_gained(caster.ability_breakdown, "Reclamation (Holy Shock)", reclamation_mana)
                
            # reset light of the martyr & bestow light
            if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
                self.spell_healing_modifier /= cumulative_healing_mod
                
                light_of_the_martyr_negative_healing = heal_amount * 0.3 * -1
                target = targets[0]
                target.receive_heal(light_of_the_martyr_negative_healing, caster)
                
                update_spell_data_heals(caster.ability_breakdown, "Light of the Martyr ", target, light_of_the_martyr_negative_healing, False)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras:
                fading_light_absorb = heal_amount * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = 0.12
                if random.random() <= holy_shock_reset_chance:
                    self.reset_cooldown(caster, current_time)
     
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.12
                    
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
                if caster.set_bonuses["dragonflight_season_2"] >= 2:
                    if caster.is_talent_active("Holy Prism"):
                        handle_flat_cdr(caster.abilities["Holy Prism"], 1)
                    elif caster.is_talent_active("Light's Hammer"):
                        handle_flat_cdr(caster.abilities["Light's Hammer"], 2)
                    
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
                    
                    # glorious dawn
                    if caster.is_talent_active("Glorious Dawn"):
                        glimmer_heal_value *= 1.1
                        
                    # blessed focus    
                    if caster.is_talent_active("Blessed Focus"):
                        glimmer_heal_value *= 1.4
                    
                    total_glimmer_healing += glimmer_heal_value
                    
                    caster.total_glimmer_healing += glimmer_heal_value
                    caster.glimmer_hits += 1

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
                        
            # overflowing light
            if caster.is_talent_active("Overflowing Light"):
                overflowing_light_absorb_value = heal_amount * 0.3 * (caster.overhealing[self.name])
                targets[0].receive_heal(overflowing_light_absorb_value, caster)
                caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                
                update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", targets[0], overflowing_light_absorb_value, False)
                append_spell_heal_event(caster.events, "Overflowing Light", caster, targets[0], overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                        
            # rising sunlight  
            if caster.is_talent_active("Rising Sunlight") and initial_cast:
                if "Rising Sunlight" in caster.active_auras:
                    caster.delayed_casts.append((RisingSunlightHolyShock(caster), current_time + 0.3, targets[0]))
                    caster.delayed_casts.append((RisingSunlightHolyShock(caster), current_time + 0.6, targets[0]))
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
                        
            # barrier of faith
            if caster.is_talent_active("Barrier of Faith"):
                for target in caster.potential_healing_targets:
                    if "Barrier of Faith" in target.target_active_buffs:
                        barrier_of_faith_absorb = heal_amount * 0.2
                        target.receive_heal(barrier_of_faith_absorb, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Barrier of Faith (Holy Shock)", target, barrier_of_faith_absorb, False)
            
            # power of the silver hand            
            if caster.is_talent_active("Power of the Silver Hand") and "Power of the Silver Hand" not in caster.active_auras and "Power of the Silver Hand Stored Healing" in caster.active_auras:
                del caster.active_auras["Power of the Silver Hand Stored Healing"]     
                update_self_buff_data(caster.self_buff_breakdown, "Power of the Silver Hand Stored Healing", current_time, "expired")
                
            # tww season 1 tier 4pc
            if caster.set_bonuses["tww_season_1"] >= 4:            
                if "Pure Light" in caster.active_auras:
                    pure_light = caster.active_auras["Pure Light"]
                    
                    if pure_light.current_stacks < pure_light.max_stacks:
                        pure_light.current_stacks += 1
                    
                    pure_light.duration = pure_light.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Pure Light", current_time, "applied", pure_light.duration, pure_light.current_stacks)               
                else:
                    caster.apply_buff_to_self(PureLight(caster), current_time, stacks_to_apply=1, max_stacks=4)
                
            # second sunrise
            if caster.is_talent_active("Second Sunrise") and initial_cast:
                second_sunrise_chance = 0.15
                if random.random() <= second_sunrise_chance:
                    caster.global_cooldown = 0
                    self.SPELL_POWER_COEFFICIENT *= 0.3
                    original_mana_cost = self.MANA_COST
                    self.MANA_COST = 0
                    self.mana_cost = 0
                    self.current_charges += 1
                    
                    self.cast_healing_spell(caster, targets, current_time, is_heal, glimmer_targets, initial_cast=False)
                    
                    self.SPELL_POWER_COEFFICIENT /= 0.3                  
                    self.MANA_COST = original_mana_cost
                    self.mana_cost = original_mana_cost
                    caster.global_cooldown = caster.base_global_cooldown / caster.haste_multiplier
                    
                    return
                            
            return cast_success, spell_crit, heal_amount, total_glimmer_healing, barrier_of_faith_absorb
            
            
class Daybreak(Spell):
    
    BASE_COOLDOWN = 60
    
    def __init__(self, caster):
        super().__init__("Daybreak", cooldown=Daybreak.BASE_COOLDOWN) 
        if caster.set_bonuses["dragonflight_season_3"] >= 4: 
            self.BASE_COOLDOWN = 45
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        total_glimmer_healing = 0
        if cast_success:
            caster.events.append(f"{format_time(current_time)}: {caster.name} cast {self.name}")
            
            number_of_glimmers_removed = len(glimmer_targets)
            caster.glimmer_removal_counter += number_of_glimmers_removed
            if caster.ptr:
                daybreak_mana_gain = 35000 * number_of_glimmers_removed
            else:
                daybreak_mana_gain = 2000 * number_of_glimmers_removed
            caster.mana += daybreak_mana_gain
            update_mana_gained(caster.ability_breakdown, "Daybreak", daybreak_mana_gain)
            
            # rising sunlight
            if caster.is_talent_active("Rising Sunlight"):
                caster.apply_buff_to_self(RisingSunlight(caster), current_time, stacks_to_apply=3, max_stacks=3)
            
            # tier season 3 4pc  
            if caster.set_bonuses["dragonflight_season_3"] >= 4:
                caster.apply_buff_to_self(FirstLight(), current_time)
            
            # adjust for daybreak 200% glimmer healing
            for glimmer_target in glimmer_targets:
                glimmer_heal, glimmer_crit = GlimmerOfLightSpell(caster).calculate_heal(caster)
                glimmer_heal_value = 2 * glimmer_heal
                
                # glorious dawn
                if caster.is_talent_active("Glorious Dawn"):
                    glimmer_heal_value *= 1.1
                    
                # blessed focus    
                if caster.is_talent_active("Blessed Focus"):
                    glimmer_heal_value *= 1.4    
                    
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
                
                if caster.set_bonuses["dragonflight_season_3"] >= 2:
                    target.apply_buff_to_target(HolyReverberation(caster), current_time, caster=caster)
                    
                    longest_reverberation_duration = max(buff_instance.duration for buff_instance in target.target_active_buffs["Holy Reverberation"]) if "Holy Reverberation" in target.target_active_buffs and target.target_active_buffs["Holy Reverberation"] else None
                    if "Holy Reverberation" in target.target_active_buffs:
                        if len(target.target_active_buffs["Holy Reverberation"]) > 0:
                            caster.buff_events.append(f"{format_time(current_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
        
        return cast_success, spell_crit, heal_amount, total_glimmer_healing
            
               
class RisingSunlightHolyShock(Spell):
    
    SPELL_POWER_COEFFICIENT = 2.266
    HOLY_POWER_GAIN = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock (Rising Sunlight)", base_mana_cost=HolyShock.BASE_MANA_COST, holy_power_gain=RisingSunlightHolyShock.HOLY_POWER_GAIN, is_heal=True, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets, initial_cast=True):
        bonus_crit = 0
        
        # tww season 1 tier 2pc
        if caster.set_bonuses["tww_season_1"] >= 2:
            self.spell_healing_modifier *= 1.1
        
        # blessing of an'she
        if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
            self.spell_healing_modifier *= 3
        
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            bonus_crit += 0.08      
             
        # luminosity    
        if caster.is_talent_active("Luminosity"):
            bonus_crit += 0.05
        
        self.bonus_crit = HolyShock.BONUS_CRIT + bonus_crit
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.12
            
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
            
        # light of the martyr & bestow light    
        if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
            cumulative_healing_mod = 1.2
            if caster.is_talent_active("Bestow Light") and "Bestow Light" in caster.active_auras:
                cumulative_healing_mod += 0.05 * caster.active_auras["Bestow Light"].current_stacks
            self.spell_healing_modifier *= cumulative_healing_mod
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal, exclude_cast=not initial_cast, initial_cast=initial_cast)
        barrier_of_faith_absorb = 0
        if cast_success:
            # tww season 1 tier 2pc
            if caster.set_bonuses["tww_season_1"] >= 2:
                self.spell_healing_modifier /= 1.1
            
            # blessing of an'she
            if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
                self.spell_healing_modifier /= 3
                del caster.active_auras["Blessing of An'she"]
                update_self_buff_data(caster.self_buff_breakdown, "Blessing of An'she", current_time, "expired")
                
            # sun sear
            if spell_crit and caster.is_talent_active("Sun Sear"):
                targets[0].apply_buff_to_target(SunSear(caster), current_time, caster=caster)
            
            # reset light of the martyr & bestow light
            if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
                self.spell_healing_modifier /= cumulative_healing_mod
                
                light_of_the_martyr_negative_healing = heal_amount * 0.3 * -1
                target = targets[0]
                target.receive_heal(light_of_the_martyr_negative_healing, caster)
                
                update_spell_data_heals(caster.ability_breakdown, "Light of the Martyr ", target, light_of_the_martyr_negative_healing, False)
            
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
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras:
                fading_light_absorb = heal_amount * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = 0.12
                if random.random() <= holy_shock_reset_chance:
                    caster.abilities["Holy Shock"].reset_cooldown(caster, current_time)
            
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.12
                    
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
                if caster.set_bonuses["dragonflight_season_2"] >= 2:
                    if caster.is_talent_active("Holy Prism"):
                        handle_flat_cdr(caster.abilities["Holy Prism"], 1)
                    elif caster.is_talent_active("Light's Hammer"):
                        handle_flat_cdr(caster.abilities["Light's Hammer"], 2)
                
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
                    
                    # glorious dawn
                    if caster.is_talent_active("Glorious Dawn"):
                        glimmer_heal_value *= 1.1
                        
                    # blessed focus    
                    if caster.is_talent_active("Blessed Focus"):
                        glimmer_heal_value *= 1.4
                        
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
                        
            # overflowing light
            if caster.is_talent_active("Overflowing Light"):
                overflowing_light_absorb_value = heal_amount * 0.3 * (caster.overhealing[self.name])
                targets[0].receive_heal(overflowing_light_absorb_value, caster)
                caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                
                update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", targets[0], overflowing_light_absorb_value, False)
                append_spell_heal_event(caster.events, "Overflowing Light", caster, targets[0], overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                        
            # barrier of faith
            if caster.is_talent_active("Barrier of Faith"):
                for target in caster.potential_healing_targets:
                    if "Barrier of Faith" in target.target_active_buffs:
                        barrier_of_faith_absorb = heal_amount * 0.2
                        target.receive_heal(barrier_of_faith_absorb, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Barrier of Faith (Holy Shock)", target, barrier_of_faith_absorb, False)
                        
            # power of the silver hand            
            if caster.is_talent_active("Power of the Silver Hand") and "Power of the Silver Hand" not in caster.active_auras and "Power of the Silver Hand Stored Healing" in caster.active_auras:
                del caster.active_auras["Power of the Silver Hand Stored Healing"]     
                update_self_buff_data(caster.self_buff_breakdown, "Power of the Silver Hand Stored Healing", current_time, "expired")
                
            # tww season 1 tier 4pc
            if caster.set_bonuses["tww_season_1"] >= 4:            
                if "Pure Light" in caster.active_auras:
                    pure_light = caster.active_auras["Pure Light"]
                    
                    if pure_light.current_stacks < pure_light.max_stacks:
                        pure_light.current_stacks += 1
                    
                    pure_light.duration = pure_light.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Pure Light", current_time, "applied", pure_light.duration, pure_light.current_stacks)               
                else:
                    caster.apply_buff_to_self(PureLight(caster), current_time, stacks_to_apply=1, max_stacks=4)
                
            # second sunrise
            if caster.is_talent_active("Second Sunrise"):
                second_sunrise_chance = 0.15
                if random.random() <= second_sunrise_chance:
                    holy_shock = self
                    
                    caster.global_cooldown = 0
                    holy_shock.SPELL_POWER_COEFFICIENT *= 0.3
                    holy_shock.current_charges += 1
                    
                    holy_shock.cast_healing_spell(caster, targets, current_time, is_heal, glimmer_targets, initial_cast=False)
                    
                    holy_shock.SPELL_POWER_COEFFICIENT /= 0.3                  
                    caster.global_cooldown = caster.base_global_cooldown / caster.haste_multiplier
                    
                    return
                        
        return cast_success, spell_crit, heal_amount, total_glimmer_healing, barrier_of_faith_absorb
            
                    
class DivineToll(Spell):
    
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
                
            # rising sunlight
            if caster.is_talent_active("Rising Sunlight"):
                caster.apply_buff_to_self(RisingSunlight(caster), current_time, stacks_to_apply=2, max_stacks=4)
                
        return cast_success, spell_crit, heal_amount   
  
  
class DivineTollHolyShock(Spell):
    
    SPELL_POWER_COEFFICIENT = 2.266
    HOLY_POWER_GAIN = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock (Divine Toll)", base_mana_cost=HolyShock.BASE_MANA_COST, holy_power_gain=DivineTollHolyShock.HOLY_POWER_GAIN, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets, initial_cast=True):
        bonus_crit = 0
        
        # tww season 1 tier 2pc
        if caster.set_bonuses["tww_season_1"] >= 2:
            self.spell_healing_modifier *= 1.1
        
        # blessing of an'she
        if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
            self.spell_healing_modifier *= 3
        
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            bonus_crit += 0.08      
             
        # luminosity    
        if caster.is_talent_active("Luminosity"):
            bonus_crit += 0.05
        
        self.bonus_crit = HolyShock.BONUS_CRIT + bonus_crit
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20

        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.12
            
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
            
        # light of the martyr & bestow light    
        if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
            cumulative_healing_mod = 1.2
            if caster.is_talent_active("Bestow Light") and "Bestow Light" in caster.active_auras:
                cumulative_healing_mod += 0.05 * caster.active_auras["Bestow Light"].current_stacks
            self.spell_healing_modifier *= cumulative_healing_mod
            
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal, exclude_cast=not initial_cast, initial_cast=initial_cast)
        total_glimmer_healing = 0
        barrier_of_faith_absorb = 0
        if cast_success:
            # tww season 1 tier 2pc
            if caster.set_bonuses["tww_season_1"] >= 2:
                self.spell_healing_modifier /= 1.1
            
            # blessing of an'she
            if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
                self.spell_healing_modifier /= 3
                del caster.active_auras["Blessing of An'she"]
                update_self_buff_data(caster.self_buff_breakdown, "Blessing of An'she", current_time, "expired")
                
            # sun sear
            if spell_crit and caster.is_talent_active("Sun Sear"):
                targets[0].apply_buff_to_target(SunSear(caster), current_time, caster=caster)
            
            # reset light of the martyr & bestow light
            if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
                self.spell_healing_modifier /= cumulative_healing_mod
                
                light_of_the_martyr_negative_healing = heal_amount * 0.3 * -1
                target = targets[0]
                target.receive_heal(light_of_the_martyr_negative_healing, caster)
                
                update_spell_data_heals(caster.ability_breakdown, "Light of the Martyr ", target, light_of_the_martyr_negative_healing, False)
            
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
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras:
                fading_light_absorb = heal_amount * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = 0.12
                if random.random() <= holy_shock_reset_chance:
                    caster.abilities["Holy Shock"].reset_cooldown(caster, current_time)
            
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.12
                    
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
                if caster.set_bonuses["dragonflight_season_2"] >= 2:
                    if caster.is_talent_active("Holy Prism"):
                        handle_flat_cdr(caster.abilities["Holy Prism"], 1)
                    elif caster.is_talent_active("Light's Hammer"):
                        handle_flat_cdr(caster.abilities["Light's Hammer"], 2)
                
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
                        
                    # blessed focus    
                    if caster.is_talent_active("Blessed Focus"):
                        glimmer_heal_value *= 1.4   

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
                    
            # overflowing light
            if caster.is_talent_active("Overflowing Light"):
                overflowing_light_absorb_value = heal_amount * 0.3 * (caster.overhealing[self.name])
                targets[0].receive_heal(overflowing_light_absorb_value, caster)
                caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                
                update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", targets[0], overflowing_light_absorb_value, False)
                append_spell_heal_event(caster.events, "Overflowing Light", caster, targets[0], overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                    
            # barrier of faith
            if caster.is_talent_active("Barrier of Faith"):
                for target in caster.potential_healing_targets:
                    if "Barrier of Faith" in target.target_active_buffs:
                        barrier_of_faith_absorb = heal_amount * 0.2
                        target.receive_heal(barrier_of_faith_absorb, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Barrier of Faith (Holy Shock)", target, barrier_of_faith_absorb, False)
                        
            # power of the silver hand            
            if caster.is_talent_active("Power of the Silver Hand") and "Power of the Silver Hand" not in caster.active_auras and "Power of the Silver Hand Stored Healing" in caster.active_auras:
                del caster.active_auras["Power of the Silver Hand Stored Healing"]     
                update_self_buff_data(caster.self_buff_breakdown, "Power of the Silver Hand Stored Healing", current_time, "expired")
                
            # tww season 1 tier 4pc
            if caster.set_bonuses["tww_season_1"] >= 4:            
                if "Pure Light" in caster.active_auras:
                    pure_light = caster.active_auras["Pure Light"]
                    
                    if pure_light.current_stacks < pure_light.max_stacks:
                        pure_light.current_stacks += 1
                    
                    pure_light.duration = pure_light.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Pure Light", current_time, "applied", pure_light.duration, pure_light.current_stacks)               
                else:
                    caster.apply_buff_to_self(PureLight(caster), current_time, stacks_to_apply=1, max_stacks=4)
                
            # second sunrise
            if caster.is_talent_active("Second Sunrise"):
                second_sunrise_chance = 0.15
                if random.random() <= second_sunrise_chance:
                    holy_shock = self
                    
                    caster.global_cooldown = 0
                    holy_shock.SPELL_POWER_COEFFICIENT *= 0.3
                    holy_shock.current_charges += 1
                    
                    holy_shock.cast_healing_spell(caster, targets, current_time, is_heal, glimmer_targets, initial_cast=False)
                    
                    holy_shock.SPELL_POWER_COEFFICIENT /= 0.3                  
                    caster.global_cooldown = caster.base_global_cooldown / caster.haste_multiplier
                    
                    return
                    
        return cast_success, spell_crit, heal_amount, total_glimmer_healing, barrier_of_faith_absorb
            
            
class DivineResonanceHolyShock(Spell):
    
    SPELL_POWER_COEFFICIENT = 2.266
    HOLY_POWER_GAIN = 1
    BONUS_CRIT = 0.1
    
    def __init__(self, caster):
        super().__init__("Holy Shock (Divine Resonance)", base_mana_cost=HolyShock.BASE_MANA_COST, holy_power_gain=DivineTollHolyShock.HOLY_POWER_GAIN, is_heal=True, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, glimmer_targets, initial_cast=True):
        bonus_crit = 0
        
        # tww season 1 tier 2pc
        if caster.set_bonuses["tww_season_1"] >= 2:
            self.spell_healing_modifier *= 1.1
        
        # blessing of an'she
        if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
            self.spell_healing_modifier *= 3
        
        # divine glimpse
        if caster.is_talent_active("Divine Glimpse"):
            bonus_crit += 0.08      
             
        # luminosity    
        if caster.is_talent_active("Luminosity"):
            bonus_crit += 0.05
        
        self.bonus_crit = HolyShock.BONUS_CRIT + bonus_crit
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.12
                      
        # reclamation
        if caster.is_talent_active("Reclamation"):
            self.spell_healing_modifier *= ((1 - caster.average_raid_health_percentage) * 0.5) + 1
            
        # light of the martyr & bestow light    
        if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
            cumulative_healing_mod = 1.2
            if caster.is_talent_active("Bestow Light") and "Bestow Light" in caster.active_auras:
                cumulative_healing_mod += 0.05 * caster.active_auras["Bestow Light"].current_stacks
            self.spell_healing_modifier *= cumulative_healing_mod
            
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal, exclude_cast=not initial_cast, initial_cast=initial_cast)
        barrier_of_faith_absorb = 0
        if cast_success:
            # tww season 1 tier 2pc
            if caster.set_bonuses["tww_season_1"] >= 2:
                self.spell_healing_modifier /= 1.1
            
            # blessing of an'she
            if caster.is_talent_active("Blessing of An'she") and "Blessing of An'she" in caster.active_auras:
                self.spell_healing_modifier /= 3
                del caster.active_auras["Blessing of An'she"]
                update_self_buff_data(caster.self_buff_breakdown, "Blessing of An'she", current_time, "expired")
              
            # sun sear
            if spell_crit and caster.is_talent_active("Sun Sear"):
                targets[0].apply_buff_to_target(SunSear(caster), current_time, caster=caster)
            
            # reset light of the martyr & bestow light
            if caster.is_talent_active("Light of the Martyr") and "Light of the Martyr" in caster.active_auras:
                self.spell_healing_modifier /= cumulative_healing_mod
                
                light_of_the_martyr_negative_healing = heal_amount * 0.3 * -1
                target = targets[0]
                target.receive_heal(light_of_the_martyr_negative_healing, caster)
                
                update_spell_data_heals(caster.ability_breakdown, "Light of the Martyr ", target, light_of_the_martyr_negative_healing, False)
            
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
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras:
                fading_light_absorb = heal_amount * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            # glorious dawn
            if caster.is_talent_active("Glorious Dawn"):
                holy_shock_reset_chance = 0.12
                if random.random() <= holy_shock_reset_chance:
                    caster.abilities["Holy Shock"].reset_cooldown(caster, current_time)
            
            # tyr's deliverance extension
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.12
                    
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
                if caster.set_bonuses["dragonflight_season_2"] >= 2:
                    if caster.is_talent_active("Holy Prism"):
                        handle_flat_cdr(caster.abilities["Holy Prism"], 1)
                    elif caster.is_talent_active("Light's Hammer"):
                        handle_flat_cdr(caster.abilities["Light's Hammer"], 2)
                
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
                        
            # overflowing light
            if caster.is_talent_active("Overflowing Light"):
                overflowing_light_absorb_value = heal_amount * 0.3 * (caster.overhealing[self.name])
                targets[0].receive_heal(overflowing_light_absorb_value, caster)
                caster.healing_by_ability["Overflowing Light"] = caster.healing_by_ability.get("Overflowing Light", 0) + overflowing_light_absorb_value
                
                update_spell_data_heals(caster.ability_breakdown, "Overflowing Light", targets[0], overflowing_light_absorb_value, False)
                append_spell_heal_event(caster.events, "Overflowing Light", caster, targets[0], overflowing_light_absorb_value, current_time, is_crit=False, is_absorb=True)
                        
            # barrier of faith
            if caster.is_talent_active("Barrier of Faith"):
                for target in caster.potential_healing_targets:
                    if "Barrier of Faith" in target.target_active_buffs:
                        barrier_of_faith_absorb = heal_amount * 0.2
                        target.receive_heal(barrier_of_faith_absorb, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Barrier of Faith (Holy Shock)", target, barrier_of_faith_absorb, False)
                        
            # power of the silver hand            
            if caster.is_talent_active("Power of the Silver Hand") and "Power of the Silver Hand" not in caster.active_auras and "Power of the Silver Hand Stored Healing" in caster.active_auras:
                del caster.active_auras["Power of the Silver Hand Stored Healing"]     
                update_self_buff_data(caster.self_buff_breakdown, "Power of the Silver Hand Stored Healing", current_time, "expired")
                
            # tww season 1 tier 4pc
            if caster.set_bonuses["tww_season_1"] >= 4:            
                if "Pure Light" in caster.active_auras:
                    pure_light = caster.active_auras["Pure Light"]
                    
                    if pure_light.current_stacks < pure_light.max_stacks:
                        pure_light.current_stacks += 1
                    
                    pure_light.duration = pure_light.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Pure Light", current_time, "applied", pure_light.duration, pure_light.current_stacks)               
                else:
                    caster.apply_buff_to_self(PureLight(caster), current_time, stacks_to_apply=1, max_stacks=4)
                
            # second sunrise
            if caster.is_talent_active("Second Sunrise"):
                second_sunrise_chance = 0.15
                if random.random() <= second_sunrise_chance:
                    holy_shock = self
                    
                    caster.global_cooldown = 0
                    holy_shock.SPELL_POWER_COEFFICIENT *= 0.3
                    holy_shock.current_charges += 1
                    
                    holy_shock.cast_healing_spell(caster, targets, current_time, is_heal, glimmer_targets, initial_cast=False)
                    
                    holy_shock.SPELL_POWER_COEFFICIENT /= 0.3                  
                    caster.global_cooldown = caster.base_global_cooldown / caster.haste_multiplier
                    
                    return
                        
        return cast_success, spell_crit, heal_amount, 0, barrier_of_faith_absorb


class HolyLight(Spell):
    
    SPELL_POWER_COEFFICIENT = 3.8
    MANA_COST = 0.064
    HOLY_POWER_GAIN = 0
    BASE_CAST_TIME = 2
    
    def __init__(self, caster):
        super().__init__("Holy Light", base_mana_cost=HolyLight.MANA_COST, holy_power_gain=HolyLight.HOLY_POWER_GAIN, base_cast_time=HolyLight.BASE_CAST_TIME, is_heal=True)
        # tower of radiance
        if caster.is_talent_active("Tower of Radiance"):
            self.holy_power_gain = 1
    
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # tyr's deliverance
        if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
            self.spell_healing_modifier *= 1.12
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # infusion of light & inflorescence of the sunwell
        if "Infusion of Light" in caster.active_auras:  
            if caster.is_talent_active("Inflorescence of the Sunwell"):
                self.spell_healing_modifier *= 2.5
            else:
                self.spell_healing_modifier *= 2
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        resplendent_light_healing = 0
        barrier_of_faith_absorb = 0
        if cast_success:
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
                    update_mana_gained(caster.ability_breakdown, "Divine Revelations (Holy Light)", divine_revelations_mana_gain)
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras and caster.is_talent_active("Tower of Radiance"):
                fading_light_absorb = heal_amount * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            # resplendent light
            if caster.is_talent_active("Resplendent Light"):
                resplendent_light_healing = heal_amount * 0.08
                target_pool = copy.deepcopy(caster.potential_healing_targets)
                for _ in range(caster.variable_target_counts["Resplendent Light"]):
                    target = random.choice(target_pool)
                    target.receive_heal(resplendent_light_healing, caster)
                    target_pool.remove(target)
                    append_spell_heal_event(caster.events, "Resplendent Light", caster, target, resplendent_light_healing, current_time, is_crit=False) 
                    
                    update_spell_data_heals(caster.ability_breakdown, "Resplendent Light", target, resplendent_light_healing, False) 
                    
                    # beacon of light
                    caster.handle_beacon_healing("Resplendent Light", target, resplendent_light_healing, current_time)
            
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.12
                
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
                    caster.abilities["Holy Shock"].remaining_cooldown -= 1
                    
                    if caster.abilities["Holy Shock"].remaining_cooldown <= 0 and caster.is_talent_active("Light's Conviction"):
                        caster.holy_shock_cooldown_overflow = abs(caster.abilities["Holy Shock"].remaining_cooldown)
                        caster.abilities["Holy Shock"].remaining_cooldown = max(caster.abilities["Holy Shock"].calculate_cooldown(caster) - caster.holy_shock_cooldown_overflow, 0)
                        if caster.abilities["Holy Shock"].current_charges < caster.abilities["Holy Shock"].max_charges:
                            caster.abilities["Holy Shock"].current_charges += 1
                
                # handle inflorescence of the sunwell
                if caster.is_talent_active("Inflorescence of the Sunwell"):
                    self.spell_healing_modifier /= 2.5
                else:
                    self.spell_healing_modifier /= 2
                    
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
                
            else:
                increment_holy_power(self, caster, current_time)
                update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
            # remove divine favor, start divine favor spell cd
            if "Divine Favor" in caster.active_auras:
                append_aura_removed_event(caster.events, "Divine Favor", caster, caster, current_time)
            
                caster.active_auras["Divine Favor"].remove_effect(caster)
                del caster.active_auras["Divine Favor"]
                
                update_self_buff_data(caster.self_buff_breakdown, "Divine Favor", current_time, "expired")
            
            # remove hand of divinity   
            if "Hand of Divinity" in caster.active_auras:        
                caster.remove_or_decrement_buff_on_self(caster.active_auras["Hand of Divinity"], current_time)
                
                update_self_buff_data(caster.self_buff_breakdown, "Hand of Divinity", current_time, "expired")
                
            # barrier of faith
            if caster.is_talent_active("Barrier of Faith"):
                for target in caster.potential_healing_targets:
                    if "Barrier of Faith" in target.target_active_buffs:
                        barrier_of_faith_absorb = heal_amount * 0.2
                        target.receive_heal(barrier_of_faith_absorb, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Barrier of Faith (Holy Light)", target, barrier_of_faith_absorb, False)
                
        return cast_success, spell_crit, heal_amount, resplendent_light_healing, barrier_of_faith_absorb


class FlashOfLight(Spell):
    
    SPELL_POWER_COEFFICIENT = 3.156 * 0.95
    MANA_COST = 0.018 
    BASE_MANA_COST = 0.018
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
            self.spell_healing_modifier *= 1.12
            
        # moment of compassion
        if caster.is_talent_active("Moment of Compassion"):
            if targets[0] in caster.beacon_targets:
                self.spell_healing_modifier *= 1.5
        
        # awestruck   
        self.bonus_crit_healing = 0   
        if caster.is_talent_active("Awestruck"):
            self.bonus_crit_healing += 20
        
        # divine revelations
        if caster.is_talent_active("Divine Revelations"):
            if "Infusion of Light" in caster.active_auras:
                self.spell_healing_modifier *= 1.2
            
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        barrier_of_faith_absorb = 0
        if cast_success:
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
            
            # blessing of dawn
            if caster.is_talent_active("Of Dusk and Dawn"):
                caster.blessing_of_dawn_counter += 1
                if caster.blessing_of_dawn_counter == 3:
                    caster.apply_buff_to_self(BlessingOfDawn(), current_time, stacks_to_apply=1, max_stacks=2)
                    caster.blessing_of_dawn_counter = 0
                    
            # fading light
            if caster.is_talent_active("Fading Light") and "Blessing of Dusk" in caster.active_auras and caster.is_talent_active("Tower of Radiance"):
                fading_light_absorb = heal_amount * 0.03
                caster.receive_self_heal(fading_light_absorb)
                update_spell_data_heals(caster.ability_breakdown, "Fading Light", caster, fading_light_absorb, False)
            
            if "Tyr's Deliverance (target)" in targets[0].target_active_buffs:
                self.spell_healing_modifier /= 1.12
                
                # boundless salvation
                if caster.is_talent_active("Boundless Salvation"):
                    if "Tyr's Deliverance (self)" in caster.active_auras:
                        if caster.tyrs_deliverance_extended_by <= 36:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 4)
                            caster.tyrs_deliverance_extended_by += 4
                        elif 36 < caster.tyrs_deliverance_extended_by < 40:
                            caster.extend_buff_on_self(caster.active_auras["Tyr's Deliverance (self)"], current_time, 40 - caster.tyrs_deliverance_extended_by)
                            caster.tyrs_deliverance_extended_by += 40 - caster.tyrs_deliverance_extended_by
                            
            if caster.is_talent_active("Moment of Compassion"):
                if targets[0] in caster.beacon_targets:
                    self.spell_healing_modifier /= 1.5
            
            increment_holy_power(self, caster, current_time)
            update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
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
                
            # remove divine favor
            if "Divine Favor" in caster.active_auras:
                append_aura_removed_event(caster.events, "Divine Favor", caster, caster, current_time)

                caster.active_auras["Divine Favor"].remove_effect(caster)
                del caster.active_auras["Divine Favor"]
                
                update_self_buff_data(caster.self_buff_breakdown, "Divine Favor", current_time, "expired")
                
            # barrier of faith
            if caster.is_talent_active("Barrier of Faith"):
                for target in caster.potential_healing_targets:
                    if "Barrier of Faith" in target.target_active_buffs:
                        barrier_of_faith_absorb = heal_amount * 0.2
                        target.receive_heal(barrier_of_faith_absorb, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Barrier of Faith (Flash of Light)", target, barrier_of_faith_absorb, False)
                
        return cast_success, spell_crit, heal_amount, barrier_of_faith_absorb
                
            
# spenders
class WordOfGlory(Spell):
    
    SPELL_POWER_COEFFICIENT = 3.15 * 1.58 * 1.1
    MANA_COST = 0.006
    HOLY_POWER_COST = 3
    BASE_COOLDOWN = 0
    
    def __init__(self, caster):
        super().__init__("Word of Glory", mana_cost=WordOfGlory.MANA_COST, holy_power_cost=WordOfGlory.HOLY_POWER_COST, max_charges=0, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # extrication
        if caster.is_talent_active("Extrication"):
            raid_health = caster.average_raid_health_percentage
            self.bonus_crit = 0.3 - (0.3 * raid_health)
        
        # gleaming rays
        if caster.is_talent_active("Gleaming Rays"):
            self.spell_healing_modifier *= 1.05
        
        # divine purpose
        if caster.is_talent_active("Divine Purpose"): 
            if "Divine Purpose" in caster.active_auras:
                self.spell_healing_modifier *= 1.15
                self.holy_power_cost = 0
                self.mana_cost = 0
            
        # apply blessing of dawn healing
        if caster.is_talent_active("Of Dusk and Dawn"):
            if "Blessing of Dawn" in caster.active_auras:
                if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                    self.spell_healing_modifier *= 1.1
                elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                    self.spell_healing_modifier *= 1.2
        
        # unending light
        unending_light_modifier = 1           
        if caster.is_talent_active("Unending Light") and "Unending Light" in caster.active_auras:
            unending_light_modifier = 1 + (0.05 * caster.active_auras["Unending Light"].current_stacks)
            self.spell_healing_modifier *= unending_light_modifier
            
        # strength of conviction
        strength_of_conviction_modifier = 1        
        if caster.is_talent_active("Strength of Conviction"):
            consecration_active = False
            for summon_name, summon_instance in caster.active_summons.items():
                if summon_name.startswith("Consecration"):
                    consecration_active = True
            if consecration_active and caster.class_talents["row8"]["Strength of Conviction"]["ranks"]["current rank"] == 1:
                strength_of_conviction_modifier *= 1.1
            elif consecration_active and caster.class_talents["row8"]["Strength of Conviction"]["ranks"]["current rank"] == 2:
                strength_of_conviction_modifier *= 1.2
        self.spell_healing_modifier *= strength_of_conviction_modifier
        
        # tww season 1 tier 4pc
        if caster.set_bonuses["tww_season_1"] >= 4:            
            if "Pure Light" in caster.active_auras:
                self.spell_healing_modifier *= 1 + (0.08 * caster.active_auras["Pure Light"].current_stacks)
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        total_glimmer_healing = 0
        afterimage_heal = 0
        empyrean_legacy_light_of_dawn_healing = 0
        if cast_success:
            caster.holy_power -= self.holy_power_cost
            
            # tww season 1 tier 4pc
            if caster.set_bonuses["tww_season_1"] >= 4:            
                if "Pure Light" in caster.active_auras:
                    self.spell_healing_modifier /= 1 + (0.08 * caster.active_auras["Pure Light"].current_stacks)
                    del caster.active_auras["Pure Light"]
                    update_self_buff_data(caster.self_buff_breakdown, "Pure Light", current_time, "expired")
            
            # tirion's devotion
            if caster.is_talent_active("Tirion's Devotion"):
                if "Divine Purpose" in caster.active_auras:
                    handle_flat_cdr(caster.abilities["Lay on Hands"], 1.5 * 3)
                else:
                    handle_flat_cdr(caster.abilities["Lay on Hands"], 1.5 * self.holy_power_cost)
                    
            # gleaming rays
            if caster.is_talent_active("Gleaming Rays"):
                self.spell_healing_modifier /= 1.05
            
            # reset healing modifier, remove blessing of dawn, and apply blessing of dusk
            if caster.is_talent_active("Of Dusk and Dawn"):
                if "Blessing of Dawn" in caster.active_auras:
                    if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                        self.spell_healing_modifier /= 1.1
                    elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                        self.spell_healing_modifier /= 1.2
                    del caster.active_auras["Blessing of Dawn"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Blessing of Dawn", current_time, "expired")
                    append_aura_removed_event(caster.buff_events, "Blessing of Dawn", caster, caster, current_time)
                    caster.apply_buff_to_self(BlessingOfDusk(), current_time, reapply=True)
                    
            # strength of conviction
            if caster.is_talent_active("Strength of Conviction"):
                self.spell_healing_modifier /= strength_of_conviction_modifier
            
            # unending light        
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
                                
                            # blessed focus    
                            if caster.is_talent_active("Blessed Focus"):
                                glimmer_heal_value *= 1.4   
                                
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
            
            # glistening radiance
            if caster.is_talent_active("Glistening Radiance"):
                random_num = random.random()
                if random_num <= 0.25:
                    for saved_by_the_light_target in caster.beacon_targets:
                        saved_by_the_light_heal = caster.spell_power * 3 * caster.versatility_multiplier
                        saved_by_the_light_target.receive_heal(saved_by_the_light_heal, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Saved by the Light (Word of Glory)", saved_by_the_light_target, saved_by_the_light_heal, False)
            
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
                    
                    update_spell_data_heals(caster.ability_breakdown, "Afterimage (Word of Glory)", targets[0], afterimage_heal, afterimage_crit)
                    append_spell_heal_event(caster.events, "Afterimage (Word of Glory)", caster, targets[0], afterimage_heal, current_time, is_crit=False)
                    
                    # beacon of light
                    caster.handle_beacon_healing("Afterimage (Word of Glory)", targets[0], afterimage_heal, current_time)
            
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
                    caster.apply_buff_to_self(caster.active_auras["Awakening"], current_time, stacks_to_apply=1, max_stacks=15)
                    if caster.active_auras["Awakening"].current_stacks >= 15:
                        del caster.active_auras["Awakening"]
                        
                        update_self_buff_data(caster.self_buff_breakdown, "Awakening", current_time, "expired")
                        append_aura_removed_event(caster.events, "Awakening", caster, caster, current_time)
                        caster.apply_buff_to_self(AwakeningTrigger(), current_time)
                        caster.awakening_trigger_times.update({round(current_time): 1})
                else:
                    caster.apply_buff_to_self(AwakeningStacks(), current_time, stacks_to_apply=1, max_stacks=15)
            
            # empyrean legacy        
            if caster.is_talent_active("Empyrean Legacy") and "Empyrean Legacy" in caster.active_auras:
                light_of_dawn = caster.abilities["Light of Dawn"]

                non_beacon_targets = [target for target in caster.potential_healing_targets if "Beacon of Light" not in target.target_active_buffs]
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
                    
            # dawnlight
            if caster.is_talent_active("Dawnlight") and "Dawnlight" in caster.active_auras:
                if "Dawnlight (HoT)" in targets[0].target_active_buffs:
                    non_dawnlight_targets = [target for target in caster.potential_healing_targets if "Dawnlight (HoT)" not in target.target_active_buffs]
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        random.choice(non_dawnlight_targets).apply_buff_to_target(Dawnlight(caster, 8 * 1.2), current_time, caster=caster)
                    else:
                        random.choice(non_dawnlight_targets).apply_buff_to_target(Dawnlight(caster), current_time, caster=caster)
                else:
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        targets[0].apply_buff_to_target(Dawnlight(caster, 8 * 1.2), current_time, caster=caster)
                    else:
                        targets[0].apply_buff_to_target(Dawnlight(caster), current_time, caster=caster)
                    
                if caster.is_talent_active("Sun's Avatar"):
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        targets[0].apply_buff_to_target(SunsAvatar(caster), current_time, caster=caster)
                
                if caster.is_talent_active("Solar Grace"):
                    caster.apply_buff_to_self(SolarGrace(caster), current_time)
                
                if caster.is_talent_active("Gleaming Rays"):
                    caster.apply_buff_to_self(GleamingRays(caster), current_time, reapply=True)
                
                if "Morning Star" in caster.active_auras:
                    caster.active_auras["Morning Star"].current_stacks = 0
                
                if caster.active_auras["Dawnlight"].current_stacks > 1:
                    caster.active_auras["Dawnlight"].current_stacks -= 1
                    update_self_buff_data(caster.self_buff_breakdown, "Dawnlight", current_time, "stacks_decremented", caster.active_auras['Dawnlight'].duration, caster.active_auras["Dawnlight"].current_stacks)
                else:
                    del caster.active_auras["Dawnlight"]
                    update_self_buff_data(caster.self_buff_breakdown, "Dawnlight", current_time, "expired")
                    
            # blessed assurance    
            if caster.is_talent_active("Blessed Assurance"):
                caster.apply_buff_to_self(BlessedAssurance(caster), current_time)
                
            # divine guidance
            if caster.is_talent_active("Divine Guidance"):            
                if "Divine Guidance" in caster.active_auras:
                    divine_guidance = caster.active_auras["Divine Guidance"]
                    
                    if divine_guidance.current_stacks < divine_guidance.max_stacks:
                        divine_guidance.current_stacks += 1
                    
                    divine_guidance.duration = divine_guidance.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Divine Guidance", current_time, "applied", divine_guidance.duration, divine_guidance.current_stacks)               
                else:
                    caster.apply_buff_to_self(DivineGuidance(caster), current_time, stacks_to_apply=1, max_stacks=10)
                    
            # liberation
            if caster.is_talent_active("Liberation"):
                random_num = random.random()
                if random_num <= caster.haste_multiplier - 1:
                    caster.apply_buff_to_self(Liberation(caster), current_time)
                    
            # blessing of the forge
            if "Blessing of the Forge" in caster.active_auras:
                sacred_word_heal, sacred_word_crit = SacredWord(caster).calculate_heal(caster)
                targets[0].receive_heal(sacred_word_heal, caster)
                update_spell_data_heals(caster.ability_breakdown, "Sacred Word", targets[0], sacred_word_heal, sacred_word_crit)
                    
        return cast_success, spell_crit, heal_amount, total_glimmer_healing, afterimage_heal, empyrean_legacy_light_of_dawn_healing
 

class EternalFlame(Spell):
    
    SPELL_POWER_COEFFICIENT = 3.15 * 1.58 * 1.1
    MANA_COST = 0.006
    HOLY_POWER_COST = 3
    BASE_COOLDOWN = 0
    
    def __init__(self, caster):
        super().__init__("Eternal Flame", mana_cost=EternalFlame.MANA_COST, holy_power_cost=EternalFlame.HOLY_POWER_COST, max_charges=0, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # extrication
        if caster.is_talent_active("Extrication"):
            raid_health = caster.average_raid_health_percentage
            self.bonus_crit = 0.3 - (0.3 * raid_health)
        
        # gleaming rays
        if caster.is_talent_active("Gleaming Rays"):
            self.spell_healing_modifier *= 1.05
        
        # divine purpose
        if caster.is_talent_active("Divine Purpose"): 
            if "Divine Purpose" in caster.active_auras:
                self.spell_healing_modifier *= 1.15
                self.holy_power_cost = 0
                self.mana_cost = 0
            
        # apply blessing of dawn healing
        if caster.is_talent_active("Of Dusk and Dawn"):
            if "Blessing of Dawn" in caster.active_auras:
                if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                    self.spell_healing_modifier *= 1.1
                elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                    self.spell_healing_modifier *= 1.2
        
        # unending light
        unending_light_modifier = 1           
        if caster.is_talent_active("Unending Light") and "Unending Light" in caster.active_auras:
            unending_light_modifier = 1 + (0.05 * caster.active_auras["Unending Light"].current_stacks)
            self.spell_healing_modifier *= unending_light_modifier
            
        # strength of conviction
        strength_of_conviction_modifier = 1        
        if caster.is_talent_active("Strength of Conviction"):
            consecration_active = False
            for summon_name, summon_instance in caster.active_summons.items():
                if summon_name.startswith("Consecration"):
                    consecration_active = True
            if consecration_active and caster.class_talents["row8"]["Strength of Conviction"]["ranks"]["current rank"] == 1:
                strength_of_conviction_modifier *= 1.1
            elif consecration_active and caster.class_talents["row8"]["Strength of Conviction"]["ranks"]["current rank"] == 2:
                strength_of_conviction_modifier *= 1.2
        self.spell_healing_modifier *= strength_of_conviction_modifier
        
        # tww season 1 tier 4pc
        if caster.set_bonuses["tww_season_1"] >= 4:            
            if "Pure Light" in caster.active_auras:
                self.spell_healing_modifier *= 1 + (0.08 * caster.active_auras["Pure Light"].current_stacks)
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        total_glimmer_healing = 0
        afterimage_heal = 0
        empyrean_legacy_light_of_dawn_healing = 0
        if cast_success:
            caster.holy_power -= self.holy_power_cost
            
            # eternal flame hot
            targets[0].apply_buff_to_target(EternalFlameBuff(caster, 16), current_time, caster=caster)
            
            # tww season 1 tier 4pc
            if caster.set_bonuses["tww_season_1"] >= 4:            
                if "Pure Light" in caster.active_auras:
                    self.spell_healing_modifier /= 1 + (0.08 * caster.active_auras["Pure Light"].current_stacks)
                    del caster.active_auras["Pure Light"]
                    update_self_buff_data(caster.self_buff_breakdown, "Pure Light", current_time, "expired")
            
            # tirion's devotion
            if caster.is_talent_active("Tirion's Devotion"):
                if "Divine Purpose" in caster.active_auras:
                    handle_flat_cdr(caster.abilities["Lay on Hands"], 1.5 * 3)
                else:
                    handle_flat_cdr(caster.abilities["Lay on Hands"], 1.5 * self.holy_power_cost)
                    
            # gleaming rays
            if caster.is_talent_active("Gleaming Rays"):
                self.spell_healing_modifier /= 1.05
            
            # reset healing modifier, remove blessing of dawn, and apply blessing of dusk
            if caster.is_talent_active("Of Dusk and Dawn"):
                if "Blessing of Dawn" in caster.active_auras:
                    if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                        self.spell_healing_modifier /= 1.1
                    elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                        self.spell_healing_modifier /= 1.2
                    del caster.active_auras["Blessing of Dawn"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Blessing of Dawn", current_time, "expired")
                    append_aura_removed_event(caster.buff_events, "Blessing of Dawn", caster, caster, current_time)
                    caster.apply_buff_to_self(BlessingOfDusk(), current_time, reapply=True)
                    
            # strength of conviction
            if caster.is_talent_active("Strength of Conviction"):
                self.spell_healing_modifier /= strength_of_conviction_modifier
            
            # unending light        
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
                                
                            # blessed focus    
                            if caster.is_talent_active("Blessed Focus"):
                                glimmer_heal_value *= 1.4   
                                
                            total_glimmer_healing += glimmer_heal_value
                            
                            caster.total_glimmer_healing += glimmer_heal_value
                            caster.glimmer_hits += 1
                            
                            # see healing by target for each glimmer proc
                            # glimmer_healing.append(f"{glimmer_target.name}: {glimmer_heal_value}, {glimmer_crit}")
                            # print(glimmer_healing)
                            
                            glimmer_target.receive_heal(glimmer_heal_value, caster)
                            caster.healing_by_ability["Glimmer of Light"] = caster.healing_by_ability.get("Glimmer of Light", 0) + glimmer_heal_value
                            
                            update_spell_data_casts(caster.ability_breakdown, "Glimmer of Light (Glistening Radiance (Eternal Flame))")
                            update_spell_data_heals(caster.ability_breakdown, "Glimmer of Light (Glistening Radiance (Eternal Flame))", glimmer_target, glimmer_heal_value, glimmer_crit)
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

            # glistening radiance
            if caster.is_talent_active("Glistening Radiance"):
                random_num = random.random()
                if random_num <= 0.25:
                    for saved_by_the_light_target in caster.beacon_targets:
                        saved_by_the_light_heal = caster.spell_power * 3 * caster.versatility_multiplier
                        saved_by_the_light_target.receive_heal(saved_by_the_light_heal, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Saved by the Light (Eternal Flame)", saved_by_the_light_target, saved_by_the_light_heal, False)

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
                    
                    update_spell_data_heals(caster.ability_breakdown, "Afterimage (Eternal Flame)", targets[0], afterimage_heal, afterimage_crit)
                    append_spell_heal_event(caster.events, "Afterimage (Eternal Flame)", caster, targets[0], afterimage_heal, current_time, is_crit=False)
                    
                    # afterimage ef
                    non_ef_targets = [target for target in caster.potential_healing_targets if "Eternal Flame" not in target.target_active_buffs]
                    chosen_target = random.choice(non_ef_targets)
                    chosen_target.apply_buff_to_target(EternalFlameBuff(caster, 16), current_time, caster=caster)
                    
                    # beacon of light
                    caster.handle_beacon_healing("Afterimage (Eternal Flame)", targets[0], afterimage_heal, current_time)
            
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
                    caster.apply_buff_to_self(caster.active_auras["Awakening"], current_time, stacks_to_apply=1, max_stacks=15)
                    if caster.active_auras["Awakening"].current_stacks >= 15:
                        del caster.active_auras["Awakening"]
                        
                        update_self_buff_data(caster.self_buff_breakdown, "Awakening", current_time, "expired")
                        append_aura_removed_event(caster.events, "Awakening", caster, caster, current_time)
                        caster.apply_buff_to_self(AwakeningTrigger(), current_time)
                        caster.awakening_trigger_times.update({round(current_time): 1})
                else:
                    caster.apply_buff_to_self(AwakeningStacks(), current_time, stacks_to_apply=1, max_stacks=15)
            
            # empyrean legacy        
            if caster.is_talent_active("Empyrean Legacy") and "Empyrean Legacy" in caster.active_auras:
                light_of_dawn = caster.abilities["Light of Dawn"]

                non_beacon_targets = [target for target in caster.potential_healing_targets if "Beacon of Light" not in target.target_active_buffs]
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
                    
            # dawnlight
            if caster.is_talent_active("Dawnlight") and "Dawnlight" in caster.active_auras:
                if "Dawnlight (HoT)" in targets[0].target_active_buffs:
                    non_dawnlight_targets = [target for target in caster.potential_healing_targets if "Dawnlight (HoT)" not in target.target_active_buffs]
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        random.choice(non_dawnlight_targets).apply_buff_to_target(Dawnlight(caster, 8 * 1.2), current_time, caster=caster)
                    else:
                        random.choice(non_dawnlight_targets).apply_buff_to_target(Dawnlight(caster), current_time, caster=caster)
                else:
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        targets[0].apply_buff_to_target(Dawnlight(caster, 8 * 1.2), current_time, caster=caster)
                    else:
                        targets[0].apply_buff_to_target(Dawnlight(caster), current_time, caster=caster)
                    
                if caster.is_talent_active("Sun's Avatar"):
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        targets[0].apply_buff_to_target(SunsAvatar(caster), current_time, caster=caster)
                
                if caster.is_talent_active("Solar Grace"):
                    caster.apply_buff_to_self(SolarGrace(caster), current_time)
                
                if caster.is_talent_active("Gleaming Rays"):
                    caster.apply_buff_to_self(GleamingRays(caster), current_time, reapply=True)
                
                if "Morning Star" in caster.active_auras:
                    caster.active_auras["Morning Star"].current_stacks = 0
                
                if caster.active_auras["Dawnlight"].current_stacks > 1:
                    caster.active_auras["Dawnlight"].current_stacks -= 1
                    update_self_buff_data(caster.self_buff_breakdown, "Dawnlight", current_time, "stacks_decremented", caster.active_auras['Dawnlight'].duration, caster.active_auras["Dawnlight"].current_stacks)
                else:
                    del caster.active_auras["Dawnlight"]
                    update_self_buff_data(caster.self_buff_breakdown, "Dawnlight", current_time, "expired")
              
            # blessed assurance    
            if caster.is_talent_active("Blessed Assurance"):
                caster.apply_buff_to_self(BlessedAssurance(caster), current_time)
                
            # divine guidance
            if caster.is_talent_active("Divine Guidance"):            
                if "Divine Guidance" in caster.active_auras:
                    divine_guidance = caster.active_auras["Divine Guidance"]
                    
                    if divine_guidance.current_stacks < divine_guidance.max_stacks:
                        divine_guidance.current_stacks += 1
                    
                    divine_guidance.duration = divine_guidance.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Divine Guidance", current_time, "applied", divine_guidance.duration, divine_guidance.current_stacks)               
                else:
                    caster.apply_buff_to_self(DivineGuidance(caster), current_time, stacks_to_apply=1, max_stacks=10)
                    
            # liberation
            if caster.is_talent_active("Liberation"):
                random_num = random.random()
                if random_num <= caster.haste_multiplier - 1:
                    caster.apply_buff_to_self(Liberation(caster), current_time)
                    
        return cast_success, spell_crit, heal_amount, total_glimmer_healing, afterimage_heal, empyrean_legacy_light_of_dawn_healing
          
            
class LightOfDawn(Spell):
    
    SPELL_POWER_COEFFICIENT = 1.2
    MANA_COST = 0.006
    HOLY_POWER_COST = 3
    BASE_COOLDOWN = 0
    TARGET_COUNT = 5
    
    def __init__(self, caster):
        super().__init__("Light of Dawn", mana_cost=LightOfDawn.MANA_COST, holy_power_cost=LightOfDawn.HOLY_POWER_COST, healing_target_count=LightOfDawn.TARGET_COUNT, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, initial_cast=True):
        bonus_crit = 0

        # luminosity    
        if caster.is_talent_active("Luminosity"):
            bonus_crit += 0.05
            
        # extrication
        if caster.is_talent_active("Extrication"):
            raid_health = caster.average_raid_health_percentage
            bonus_crit += 0.3 - (0.3 * raid_health)
        
        self.bonus_crit = bonus_crit
        
        # divine purpose
        if caster.is_talent_active("Divine Purpose") and initial_cast: 
            if "Divine Purpose" in caster.active_auras:
                self.spell_healing_modifier *= 1.15
                self.holy_power_cost = 0
                self.mana_cost = 0
                
        # gleaming rays
        if caster.is_talent_active("Gleaming Rays"):
            self.spell_healing_modifier *= 1.05
                
        # apply blessing of dawn healing
        if caster.is_talent_active("Of Dusk and Dawn"):
            if "Blessing of Dawn" in caster.active_auras:
                if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                    self.spell_healing_modifier *= 1.1
                elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                    self.spell_healing_modifier *= 1.2
                    
        # tww season 1 tier 4pc
        if caster.set_bonuses["tww_season_1"] >= 4:            
            if "Pure Light" in caster.active_auras:
                self.spell_healing_modifier *= 1 + (0.08 * caster.active_auras["Pure Light"].current_stacks)
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal, exclude_cast=not initial_cast, initial_cast=initial_cast)
        total_glimmer_healing = 0
        if cast_success:
            caster.holy_power -= self.holy_power_cost
            
            # tww season 1 tier 4pc
            if caster.set_bonuses["tww_season_1"] >= 4:            
                if "Pure Light" in caster.active_auras:
                    self.spell_healing_modifier /= 1 + (0.08 * caster.active_auras["Pure Light"].current_stacks)
                    del caster.active_auras["Pure Light"]
                    update_self_buff_data(caster.self_buff_breakdown, "Pure Light", current_time, "expired")
            
            # unending light
            if caster.is_talent_active("Unending Light") and initial_cast:
                if "Unending Light" in caster.active_auras:
                    caster.apply_buff_to_self(caster.active_auras["Unending Light"], current_time, stacks_to_apply=3, max_stacks=9)
                else:
                    caster.apply_buff_to_self(UnendingLight(3), current_time, stacks_to_apply=3, max_stacks=9)
                    
            # tirion's devotion
            if caster.is_talent_active("Tirion's Devotion"):
                if "Divine Purpose" in caster.active_auras:
                    handle_flat_cdr(caster.abilities["Lay on Hands"], 1.5 * 3)
                else:
                    handle_flat_cdr(caster.abilities["Lay on Hands"], 1.5 * self.holy_power_cost)
                    
            # gleaming rays
            if caster.is_talent_active("Gleaming Rays"):
                self.spell_healing_modifier /= 1.05
                    
            # reset healing modifier, remove blessing of dawn, and apply blessing of dusk
            if caster.is_talent_active("Of Dusk and Dawn"):
                if "Blessing of Dawn" in caster.active_auras:
                    if caster.active_auras["Blessing of Dawn"].current_stacks == 1:
                        self.spell_healing_modifier /= 1.1
                    elif caster.active_auras["Blessing of Dawn"].current_stacks == 2:
                        self.spell_healing_modifier /= 1.2
                    del caster.active_auras["Blessing of Dawn"]
                    
                    update_self_buff_data(caster.self_buff_breakdown, "Blessing of Dawn", current_time, "expired")
                    append_aura_removed_event(caster.buff_events, "Blessing of Dawn", caster, caster, current_time)
                    caster.apply_buff_to_self(BlessingOfDusk(), current_time, reapply=True)
            
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
                                
                            # blessed focus    
                            if caster.is_talent_active("Blessed Focus"):
                                glimmer_heal_value *= 1.4   
                                
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
            
            # glistening radiance
            if caster.is_talent_active("Glistening Radiance"):
                random_num = random.random()
                if random_num <= 0.25:
                    for saved_by_the_light_target in caster.beacon_targets:
                        saved_by_the_light_heal = caster.spell_power * 3 * caster.versatility_multiplier
                        saved_by_the_light_target.receive_heal(saved_by_the_light_heal, caster)
                        update_spell_data_heals(caster.ability_breakdown, "Saved by the Light (Light of Dawn)", saved_by_the_light_target, saved_by_the_light_heal, False)
            
            # afterimage
            if caster.is_talent_active("Afterimage"):
                if "Divine Purpose" not in caster.active_auras:
                    caster.afterimage_counter += self.holy_power_cost
                caster.events.append(f"{format_time(current_time)}: Afterimage ({caster.afterimage_counter})")
            
            # divine purpose
            if caster.is_talent_active("Divine Purpose") and initial_cast: 
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
            if caster.is_talent_active("Awakening") and initial_cast:
                if "Awakening" in caster.active_auras:
                    caster.apply_buff_to_self(caster.active_auras["Awakening"], current_time, stacks_to_apply=1, max_stacks=15)
                    if caster.active_auras["Awakening"].current_stacks >= 15:
                        del caster.active_auras["Awakening"]
                        
                        update_self_buff_data(caster.self_buff_breakdown, "Awakening", current_time, "expired")
                        append_aura_removed_event(caster.events, "Awakening", caster, caster, current_time)
                        caster.apply_buff_to_self(AwakeningTrigger(), current_time)
                        caster.awakening_trigger_times.update({round(current_time): 1})
                else:
                    caster.apply_buff_to_self(AwakeningStacks(), current_time, stacks_to_apply=1, max_stacks=15)
            
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
                    
            # maraad's dying breath
            if caster.is_talent_active("Maraad's Dying Breath"):
                if "Maraad's Dying Breath" in caster.active_auras:
                    maraads_dying_breath = caster.active_auras["Maraad's Dying Breath"]
                    
                    if maraads_dying_breath.current_stacks < maraads_dying_breath.max_stacks:
                        maraads_dying_breath.current_stacks += len(targets)
                        if maraads_dying_breath.current_stacks > maraads_dying_breath.max_stacks:
                            maraads_dying_breath.current_stacks = maraads_dying_breath.max_stacks
                    
                    maraads_dying_breath.duration = maraads_dying_breath.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Maraad's Dying Breath", current_time, "applied", maraads_dying_breath.duration, maraads_dying_breath.current_stacks)                      
                else:
                    caster.apply_buff_to_self(MaraadsDyingBreath(len(targets)), current_time, stacks_to_apply=len(targets), max_stacks=5)
            
            # dawnlight        
            if caster.is_talent_active("Dawnlight") and "Dawnlight" in caster.active_auras:
                if "Dawnlight (HoT)" in targets[0].target_active_buffs:
                    non_dawnlight_targets = [target for target in caster.potential_healing_targets if "Dawnlight (HoT)" not in target.target_active_buffs]
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        random.choice(non_dawnlight_targets).apply_buff_to_target(Dawnlight(caster, 8 * 1.2), current_time, caster=caster)
                    else:
                        random.choice(non_dawnlight_targets).apply_buff_to_target(Dawnlight(caster), current_time, caster=caster)
                else:
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        targets[0].apply_buff_to_target(Dawnlight(caster, 8 * 1.2), current_time, caster=caster)
                    else:
                        targets[0].apply_buff_to_target(Dawnlight(caster), current_time, caster=caster)
                    
                if caster.is_talent_active("Sun's Avatar"):
                    if "Avenging Wrath" in caster.active_auras or "Avenging Crusader" in caster.active_auras or "Avenging Wrath (Awakening)" in caster.active_auras or "Avenging Crusader (Awakening)" in caster.active_auras:
                        targets[0].apply_buff_to_target(SunsAvatar(caster), current_time, caster=caster)
                
                if caster.is_talent_active("Solar Grace"):
                    caster.apply_buff_to_self(SolarGrace(caster), current_time)
                
                if caster.is_talent_active("Gleaming Rays"):
                    caster.apply_buff_to_self(GleamingRays(caster), current_time, reapply=True)
                
                if "Morning Star" in caster.active_auras:
                    caster.active_auras["Morning Star"].current_stacks = 0
                
                if caster.active_auras["Dawnlight"].current_stacks > 1:
                    caster.active_auras["Dawnlight"].current_stacks -= 1
                    update_self_buff_data(caster.self_buff_breakdown, "Dawnlight", current_time, "stacks_decremented", caster.active_auras['Dawnlight'].duration, caster.active_auras["Dawnlight"].current_stacks)
                else:
                    del caster.active_auras["Dawnlight"]
                    update_self_buff_data(caster.self_buff_breakdown, "Dawnlight", current_time, "expired")
                    
            # blessed assurance    
            if caster.is_talent_active("Blessed Assurance"):
                caster.apply_buff_to_self(BlessedAssurance(caster), current_time)
                
            # divine guidance
            if caster.is_talent_active("Divine Guidance"):            
                if "Divine Guidance" in caster.active_auras:
                    divine_guidance = caster.active_auras["Divine Guidance"]
                    
                    if divine_guidance.current_stacks < divine_guidance.max_stacks:
                        divine_guidance.current_stacks += 1
                    
                    divine_guidance.duration = divine_guidance.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Divine Guidance", current_time, "applied", divine_guidance.duration, divine_guidance.current_stacks)               
                else:
                    caster.apply_buff_to_self(DivineGuidance(caster), current_time, stacks_to_apply=1, max_stacks=10)
                    
            # liberation
            if caster.is_talent_active("Liberation"):
                random_num = random.random()
                if random_num <= caster.haste_multiplier - 1:
                    caster.apply_buff_to_self(Liberation(caster), current_time)
                    
            # blessing of the forge
            if "Blessing of the Forge" in caster.active_auras:
                chosen_targets = random.sample(caster.potential_healing_targets, 5)
                for target in chosen_targets:
                    radiant_aura_heal, radiant_aura_crit = RadiantAura(caster).calculate_heal(caster)
                    target.receive_heal(radiant_aura_heal, caster)
                    update_spell_data_heals(caster.ability_breakdown, "Radiant Aura", target, radiant_aura_heal, radiant_aura_crit)
            
            # second sunrise        
            if caster.is_talent_active("Second Sunrise") and initial_cast:
                second_sunrise_chance = 0.15
                if random.random() <= second_sunrise_chance:
                    caster.global_cooldown = 0
                    self.SPELL_POWER_COEFFICIENT *= 0.3
                    self.MANA_COST = 0
                    self.mana_cost = 0
                    self.holy_power_cost = 0
                    
                    self.cast_healing_spell(caster, targets, current_time, is_heal, initial_cast=False)
                    
                    self.SPELL_POWER_COEFFICIENT /= 0.3                  
                    self.MANA_COST = 0.008
                    self.mana_cost = 0.008
                    self.holy_power_cost = 3
                    
                    return    
                    
        return cast_success, spell_crit, heal_amount, total_glimmer_healing


class HolyPrism(Spell):
    
    SPELL_POWER_COEFFICIENT = 3.15
    BASE_COOLDOWN = 30
    MANA_COST = 0.026
    TARGET_COUNT = 5
    
    def __init__(self, caster):
        super().__init__("Holy Prism", mana_cost=HolyPrism.MANA_COST, cooldown=HolyPrism.BASE_COOLDOWN, healing_target_count=HolyPrism.TARGET_COUNT, is_heal=True)
        
        if caster.set_bonuses["dragonflight_season_2"] >= 4:
            self.spell_healing_modifier *= 1.4
            self.holy_power_gain = 1
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            increment_holy_power(self, caster, current_time)
            update_spell_holy_power_gain(caster.ability_breakdown, self.name, self.holy_power_gain)
            
            if caster.is_talent_active("Dawnlight"):
                caster.apply_buff_to_self(DawnlightAvailable(caster), current_time, stacks_to_apply=2, max_stacks=2)
                
            if caster.is_talent_active("Aurora"):
                caster.apply_buff_to_self(DivinePurpose(), current_time, reapply=True)
                
            if caster.is_talent_active("Divine Favor"):
                if "Divine Favor" in caster.active_auras:
                    caster.active_auras["Divine Favor"].remove_effect(caster, current_time)
                caster.apply_buff_to_self(DivineFavorBuff(), current_time)
                
            return cast_success, spell_crit, heal_amount


class LightsHammerSpell(Spell):
    
    BASE_COOLDOWN = 60
    MANA_COST = 0.036
    
    def __init__(self, caster):
        super().__init__("Light's Hammer", mana_cost=LightsHammerSpell.MANA_COST, cooldown=LightsHammerSpell.BASE_COOLDOWN)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_summon(LightsHammerSummon(caster), current_time)
                
                
class LightsHammerHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.48 * 0.8
    TARGET_COUNT = 6
    
    def __init__(self, caster):
        super().__init__("Light's Hammer", healing_target_count=caster.variable_target_counts["Light's Hammer"], off_gcd=True)
      

class GoldenPathHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.05 * 1.04
    TARGET_COUNT = 6
    
    def __init__(self, caster):
        super().__init__("Golden Path", healing_target_count=GoldenPathHeal.TARGET_COUNT, off_gcd=True)
        

class SealOfMercyHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.05 * 1.04
    TARGET_COUNT = 1
    
    def __init__(self, caster):
        super().__init__("Seal of Mercy", healing_target_count=SealOfMercyHeal.TARGET_COUNT, off_gcd=True)
        

class MercifulAurasHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.1552
    
    def __init__(self, caster):  
        super().__init__("Merciful Auras", off_gcd=True)
            

class SunsAvatarHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.162
    
    def __init__(self, caster):
        super().__init__("Sun's Avatar", off_gcd=True)
        
    
class SavedByTheLightHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 9
    
    def __init__(self, caster):
        super().__init__("Saved by the Light", off_gcd=True)
        

class LayOnHands(Spell):
    
    BASE_COOLDOWN = 600
    SPELL_POWER_COEFFICIENT = 0
    
    def __init__(self, caster):
        super().__init__("Lay on Hands", cooldown=LayOnHands.BASE_COOLDOWN, off_gcd=True)
        if caster.is_talent_active("Unbreakable Spirit"):
            self.cooldown = 420
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            lay_on_hands_healing = caster.max_health
            target = targets[0]
            target.receive_heal(lay_on_hands_healing, caster)
            
            update_spell_data_heals(caster.ability_breakdown, "Lay on Hands", target, lay_on_hands_healing, False)
            update_spell_data_casts(caster.ability_breakdown, self.name, 0, 0, self.holy_power_cost)
            
            if caster.is_talent_active("Tirion's Devotion"):
                tirions_devotion_mana_gain = caster.max_mana * 0.05
                caster.mana += tirions_devotion_mana_gain
                update_mana_gained(caster.ability_breakdown, "Tirion's Devotion", tirions_devotion_mana_gain)
                
                
class LightOfTheMartyr(Spell):
    
    SPELL_POWER_COEFFICIENT = 2.31 * 0.8
    MANA_COST = 0.016
    
    def __init__(self, caster):
        super().__init__("Light of the Martyr", is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        # untempered dedication
        if caster.is_talent_active("Untempered Dedication") and "Untempered Dedication" in caster.active_auras:
            untempered_dedication = caster.active_auras["Untempered Dedication"]
            untempered_dedication_modifier = (1 + (0.1 * untempered_dedication.current_stacks))
            self.spell_healing_modifier *= untempered_dedication_modifier
            
        # maraad's dying breath
        if caster.is_talent_active("Maraad's Dying Breath") and "Maraad's Dying Breath" in caster.active_auras:
            maraads_dying_breath = caster.active_auras["Maraad's Dying Breath"]
            maraads_dying_breath_modifier = (1 + (0.1 * maraads_dying_breath.current_stacks))
            self.spell_healing_modifier *= maraads_dying_breath_modifier
        
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            light_of_the_martyr_negative_healing = heal_amount * 0.6 * -1
            target = targets[0]
            target.receive_heal(light_of_the_martyr_negative_healing, caster)
            
            update_spell_data_heals(caster.ability_breakdown, "Light of the Martyr ", target, light_of_the_martyr_negative_healing, False)
            
            # untempered dedication
            if caster.is_talent_active("Untempered Dedication"):
                if "Untempered Dedication" in caster.active_auras:
                    untempered_dedication = caster.active_auras["Untempered Dedication"]
                    self.spell_healing_modifier /= (1 + (0.1 * untempered_dedication.current_stacks))    
                    
                    if untempered_dedication.current_stacks < untempered_dedication.max_stacks:
                        untempered_dedication.current_stacks += 1
                    
                    untempered_dedication.duration = untempered_dedication.base_duration
                    update_self_buff_data(caster.self_buff_breakdown, "Untempered Dedication", current_time, "applied", untempered_dedication.duration, untempered_dedication.current_stacks)                      
                else:
                    caster.apply_buff_to_self(UntemperedDedication(), current_time, stacks_to_apply=1, max_stacks=5)
                
            # maraad's dying breath
            if caster.is_talent_active("Maraad's Dying Breath") and "Maraad's Dying Breath" in caster.active_auras:
                maraads_dying_breath = caster.active_auras["Maraad's Dying Breath"]
                maraads_dying_breath_modifier = (1 + (0.1 * maraads_dying_breath.current_stacks))
                self.spell_healing_modifier /= maraads_dying_breath_modifier
                
                del caster.active_auras["Maraad's Dying Breath"]
                update_self_buff_data(caster.self_buff_breakdown, "Maraad's Dying Breath", current_time, "expired")
                
        return cast_success, spell_crit, heal_amount
    

class DivineGuidanceHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 2 * 1.04
    
    def __init__(self, caster):
        super().__init__("Divine Guidance", off_gcd=True)
        

class HammerAndAnvilHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0
    
    def __init__(self, caster):
        super().__init__("Hammer and Anvil", off_gcd=True)
        

class TruthPrevailsHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 2.7
    
    def __init__(self, caster):
        super().__init__("Truth Prevails", off_gcd=True)
        

class SacredWord(Spell):
    
    SPELL_POWER_COEFFICIENT = 1.5
    
    def __init__(self, caster):
        super().__init__("Sacred Word", off_gcd=True)
        

class RadiantAura(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.6
    
    def __init__(self, caster):
        super().__init__("Radiant Aura", off_gcd=True)