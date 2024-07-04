import random

from .auras_buffs import SunSear
from ..utils.leech_abilities import leech_abilities
from ..utils.misc_functions import format_time, append_spell_heal_event, append_spell_started_casting_event, append_spell_cast_event, append_spell_damage_event, update_spell_data_heals, update_spell_data_casts, update_target_buff_data, update_priority_breakdown
from collections import defaultdict

class Spell:
    
    def __init__(self, name, mana_cost=0, base_mana_cost=0, holy_power_gain=0, holy_power_cost=0, cooldown=0, max_charges=1,
                 hasted_cooldown=False, healing_target_count=1, damage_target_count=1, is_heal=False, is_damage_spell=False,
                 is_absorb=False, off_gcd=False, base_cast_time=0, applies_buff_to_target=False, bonus_crit=0, bonus_crit_healing=0,
                 bonus_versatility=0, bonus_mastery=0, hasted_cast_time=True):
        self.name = name
        self.mana_cost = mana_cost
        self.base_mana_cost = base_mana_cost
        self.holy_power_gain = holy_power_gain
        self.holy_power_cost = holy_power_cost
        self.cooldown = cooldown
        self.remaining_cooldown = 0
        self.hasted_cooldown = hasted_cooldown
        self.healing_target_count = healing_target_count
        self.damage_target_count = damage_target_count
        self.is_heal = is_heal
        self.is_damage_spell = is_damage_spell
        self.is_absorb = is_absorb
        self.off_gcd = off_gcd
        self.max_charges = max_charges
        self.current_charges = self.max_charges
        self.base_cast_time = base_cast_time
        self.hasted_cast_time = hasted_cast_time
        self.applies_buff_to_target = applies_buff_to_target
        
        self.spell_healing_modifier = 1.0
        self.spell_damage_modifier = 1.0
        
        self.bonus_crit = bonus_crit
        self.bonus_crit_healing = bonus_crit_healing
        self.bonus_versatility = bonus_versatility
        self.bonus_mastery = bonus_mastery
        
        self.cast_time_modifier = 1.0
        self.mana_cost_modifier = 1.0
        
        self.original_cooldown = None
        
        self.aoe_cast_counter = 0
    
    def start_cast_time(self, caster, ability, current_time):
        caster.currently_casting = ability.name
        caster.remaining_cast_time = self.calculate_cast_time(caster, ability.hasted_cast_time)
        append_spell_started_casting_event(caster.events, caster, ability, current_time)
        
        self_auras, _, total_target_aura_counts, spell_cooldowns, current_stats = self.collect_priority_breakdown_data(caster, exclude_target_auras=True)
        
        update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts, current_stats=current_stats)    
        
    def can_cast(self, caster, current_time=0):
        if caster.is_occupied:
            return False
        if self.name in ["Hammer of Wrath"] and "Avenging Wrath" not in caster.active_auras and "Veneration" not in caster.active_auras and not caster.is_enemy_below_20_percent:
            return False       
        if not self.off_gcd and caster.global_cooldown > 0:
            return False
        if self.max_charges > 0:
            if self.remaining_cooldown > 0 and self.current_charges == 0:
                return False    
        if caster.mana < self.get_mana_cost(caster):
            return False
        if hasattr(self, "holy_power_cost") and caster.holy_power < self.holy_power_cost:
            return False       
        return True
    
    def cast_damage_spell(self, caster, targets, current_time, healing_targets=None):
        if not self.can_cast(caster):         
            return False
        
        if caster.innervate_active:
            self.mana_cost = 0
        else:
            self.mana_cost = getattr(self, "MANA_COST", 0)
        
        spell_crit = False
        
        self.try_trigger_rppm_effects(caster, targets, current_time)
        self.try_trigger_conditional_effects(caster, targets, current_time)
        
        self_auras, target_auras, total_target_aura_counts, spell_cooldowns, current_stats  = self.collect_priority_breakdown_data(caster, targets)
        
        for target in targets:
            update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, target_active_auras=target_auras, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts, current_stats=current_stats)    
            
            mana_cost = self.get_mana_cost(caster)
            damage_value, is_crit = self.calculate_damage(caster, self.bonus_crit, self.bonus_versatility)
            damage_value = round(damage_value)
            target.receive_damage(damage_value)
            
            if self.healing_target_count > 0:
                caster.mana -= mana_cost / self.healing_target_count
            else:
                caster.mana -= mana_cost
            update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, self.holy_power_gain, self.holy_power_cost)
            update_spell_data_heals(caster.ability_breakdown, self.name, target, 0, is_crit)        
            
            append_spell_damage_event(caster.events, self.name, caster, target, damage_value, current_time, is_crit, spends_mana=True)     
            append_spell_cast_event(caster.ability_cast_events, self.name, caster, current_time, target) 
            
            if is_crit:
                spell_crit = True   
        
        if self.current_charges == self.max_charges:    
            self.start_cooldown(caster)
            self.current_charges -= 1
        elif self.max_charges > 0:     
            self.current_charges -= 1
        
        caster.total_casts[self.name] = caster.total_casts.get(self.name, 0) + 1
        caster.cast_sequence.append(f"{self.name}: {current_time}")

        # update haste and gcd
        if not self.off_gcd:
            caster.global_cooldown = caster.hasted_global_cooldown

        return True, spell_crit, damage_value
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal, exclude_mastery=False, ignore_spell_multiplier=False, exclude_cast=False):
        if not self.can_cast(caster):         
            return False, False, 0
    
        if caster.innervate_active:
            self.mana_cost = 0
        elif self.name in ["Word of Glory", "Light of Dawn"] and "Divine Purpose" in caster.active_auras:
            self.mana_cost = 0
        else:
            self.mana_cost = getattr(self, "MANA_COST", 0)
        
        spell_crit = False
        heal_amount = 0
        ability_healing = 0
        
        self.try_trigger_rppm_effects(caster, targets, current_time)
        self.try_trigger_conditional_effects(caster, targets, current_time)
        
        self_auras, target_auras, total_target_aura_counts, spell_cooldowns, current_stats  = self.collect_priority_breakdown_data(caster, targets)
        
        # add spells that trigger other spells as a cast event and don't cost mana
        if self.name in ["Daybreak", "Arcane Torrent", "Gift of the Naaru"]:
            update_spell_data_casts(caster.ability_breakdown, self.name, self.get_mana_cost(caster), self.holy_power_gain, self.holy_power_cost)
            update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts, current_stats=current_stats)
            
        # add spells that cost mana and don't heal
        if caster.mana >= self.get_mana_cost(caster) and not is_heal: 
            if self.get_mana_cost(caster) > 0:
                update_spell_data_casts(caster.ability_breakdown, self.name, self.get_mana_cost(caster), self.holy_power_gain, self.holy_power_cost)             
            if self.name not in ["Tyr's Deliverance"]:
                update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, target_active_auras=target_auras, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts, current_stats=current_stats) 
            caster.mana -= self.get_mana_cost(caster)
                     
        # add spells that cost mana and do heal       
        elif caster.mana >= self.get_mana_cost(caster) and is_heal and not exclude_cast: 
            if self.name not in ["Tyr's Deliverance", "Light's Hammer", "Holy Shock (Divine Toll)", "Holy Shock (Rising Sunlight)", "Holy Shock (Divine Resonance)", "Flash of Light", "Golden Path", "Holy Light", "Seal of Mercy"]:
                update_priority_breakdown(caster.priority_breakdown, caster, current_time, "1", self.name, self_auras, {"mana": caster.mana, "holy_power": caster.holy_power}, target_active_auras=target_auras, remaining_cooldowns=spell_cooldowns, aura_counts=total_target_aura_counts, current_stats=current_stats)    
            
            target_count = self.healing_target_count
            if target_count > 1:  
                multi_target_healing = [f"{self.name}: ", []]            
            for target in targets:            
                # after calculate_heal, before it potentially modifies spell_crit
                healing_value, is_crit = self.calculate_heal(caster, bonus_crit=self.bonus_crit, bonus_versatility=self.bonus_versatility, bonus_mastery=self.bonus_mastery, exclude_mastery=exclude_mastery, ignore_spell_multiplier=ignore_spell_multiplier)
                
                mana_cost = self.get_mana_cost(caster)
                healing_value = round(healing_value) 
                target.receive_heal(healing_value, caster)
                if target_count > 1:
                    # deduct mana on the first instance of a multi-target spell
                    if self.aoe_cast_counter == 0:
                        self.aoe_cast_counter = target_count               
                    if self.aoe_cast_counter == target_count:
                        caster.mana -= mana_cost
                        # add spell, mana cost, holy power attributes, and increment casts
                        if self.name in ["Light's Hammer"] or exclude_cast:
                            update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost, exclude_casts=True)
                        else:
                            update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost)
                            
                    # sun sear
                    if is_crit and caster.ptr and caster.is_talent_active("Sun Sear") and self.name == "Light of Dawn":
                        target.apply_buff_to_target(SunSear(caster), current_time, caster=caster)
                        
                    self.aoe_cast_counter -= 1
                else: 
                    caster.mana -= mana_cost
                    
                    # exclude casts for certain spells
                    if self.name in ["Tyr's Deliverance"] or exclude_cast:
                        update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost, exclude_casts=True)
                    else:
                        update_spell_data_casts(caster.ability_breakdown, self.name, mana_cost, 0, self.holy_power_cost)
                
                # for detailed logging     
                caster.healing_by_ability[self.name] = caster.healing_by_ability.get(self.name, 0) + healing_value
                if is_crit:
                    spell_crit = True
                    caster.ability_crits[self.name] = caster.ability_crits.get(self.name, 0) + 1
                if target_count == 1:
                    caster.healing_sequence.append(f"{self.name}: {current_time}, {healing_value}, {is_crit}")
                else:
                    multi_target_healing[1].append([healing_value, target.name, is_crit])
                 
                if target_count > 1:  
                    for aoe_heal in multi_target_healing[1]:
                        ability_healing = aoe_heal[0]
                        heal_amount += aoe_heal[0]
                else:      
                    ability_healing = healing_value   
                    heal_amount += healing_value             
        
                # add the target, healing, crit status, and increment hits
                update_spell_data_heals(caster.ability_breakdown, self.name, target, ability_healing, is_crit)
                
                append_spell_heal_event(caster.events, self.name, caster, target, ability_healing, current_time, is_crit, spends_mana=True)   
                append_spell_cast_event(caster.ability_cast_events, self.name, caster, current_time, target)    
                
                caster.handle_beacon_healing(self.name, target, healing_value, current_time)
                   
            if self.healing_target_count > 1:
                caster.healing_sequence.append(multi_target_healing)   

        if self.current_charges == self.max_charges:
            self.start_cooldown(caster)
            self.current_charges -= 1
        elif self.max_charges > 0:     
            self.current_charges -= 1
            
        # update details
        caster.total_casts[self.name] = caster.total_casts.get(self.name, 0) + 1
        caster.cast_sequence.append(f"{self.name}: {current_time}")

        # update haste and gcd
        if not self.off_gcd:
            caster.global_cooldown = caster.hasted_global_cooldown

        return True, spell_crit, ability_healing
    
    def calculate_cast_time(self, caster, hasted=True):
        if hasted:
            return (self.base_cast_time / caster.haste_multiplier) * self.cast_time_modifier
        else:
            return self.base_cast_time * self.cast_time_modifier
    
    def calculate_heal(self, caster, bonus_crit=0, bonus_crit_healing=0, bonus_versatility=0, bonus_mastery=0, exclude_mastery=False, ignore_spell_multiplier=False):
        spell_power = caster.spell_power
        
        crit_multiplier = 1
        is_crit = False
        crit_chance = caster.crit + (self.bonus_crit * 100)
        caster_crit_healing_modifier = 1
        random_num = random.random() * 100
        if random_num <= crit_chance:
            crit_multiplier = 2 + (self.bonus_crit_healing / 100)
            caster_crit_healing_modifier = caster.crit_healing_modifier
            is_crit = True
        
        if exclude_mastery:
            mastery_multiplier = 1
        else:
            mastery_multiplier = 1 + ((caster.mastery_multiplier + self.bonus_mastery) - 1) * caster.mastery_effectiveness
            
        versatility_multiplier = caster.versatility_multiplier + self.bonus_versatility
        
        if ignore_spell_multiplier:
            spell_healing_modifier = 1
        else:
            spell_healing_modifier = self.spell_healing_modifier
            
        heal_amount = spell_power * self.SPELL_POWER_COEFFICIENT * caster.healing_multiplier * versatility_multiplier * crit_multiplier * mastery_multiplier * spell_healing_modifier * caster_crit_healing_modifier
        
        if self.name in ["Holy Shock", "Holy Shock (Rising Sunlight)", "Holy Shock (Divine Toll)", "Holy Shock (Divine Resonance)"] and "Power of the Silver Hand Stored Healing" in caster.active_auras:
            if is_crit:
                heal_amount += caster.active_auras["Power of the Silver Hand Stored Healing"].stored_healing * 2
            else:
                heal_amount += caster.active_auras["Power of the Silver Hand Stored Healing"].stored_healing
            caster.active_auras["Power of the Silver Hand Stored Healing"].stored_healing = 0
        
        # season 2 tier 2pc   
        if self.name in ["Holy Shock", "Holy Shock (Rising Sunlight)", "Holy Shock (Divine Toll)", "Holy Shock (Divine Resonance)"] and caster.set_bonuses["dragonflight_season_2"] >= 2 and is_crit:
            heal_amount *= 1.8
        
        if "Close to Heart" in caster.active_auras:
            heal_amount *= 1.04
            
        if "Aura Mastery" in caster.active_auras and caster.is_talent_active("Protection of Tyr"):
            heal_amount *= 1.1
            
        if caster.is_talent_active("Power of the Silver Hand") and "Power of the Silver Hand" in caster.active_auras:
            caster.active_auras["Power of the Silver Hand Stored Healing"].stored_healing += heal_amount * 0.1
            caster.active_auras["Power of the Silver Hand Stored Healing"].duration = caster.active_auras["Power of the Silver Hand Stored Healing"].base_duration
            
        if self.name in leech_abilities:   
            leech_multiplier = 0.7
            update_spell_data_heals(caster.ability_breakdown, "Leech", caster, heal_amount * (caster.leech / 100) * leech_multiplier, False)
        
        # if self.name == "Glimmer of Light":  
            
        # if "Holy Shock" in self.name:
        #     print(f"Heal amount for {self.name}, {heal_amount}")
        #     print(f"Calculating heal for {self.name}, {spell_power} * {self.SPELL_POWER_COEFFICIENT} * {caster.healing_multiplier} * {versatility_multiplier} * {crit_multiplier} * {mastery_multiplier} * {self.spell_healing_modifier} * {caster_crit_healing_modifier}")
        return heal_amount, is_crit
    
    def calculate_damage(self, caster, bonus_crit=0, bonus_versatility=0):
        spell_power = caster.spell_power
        
        crit_multiplier = 1
        is_crit = False
        crit_chance = caster.crit + (self.bonus_crit * 100)
        caster_crit_damage_modifier = 1
        random_num = random.random() * 100
        if random_num <= crit_chance:
            crit_multiplier = 2
            caster_crit_damage_modifier = caster.crit_damage_modifier
            is_crit = True
            
        versatility_multiplier = caster.versatility_multiplier + bonus_versatility
        
        return spell_power * self.SPELL_POWER_COEFFICIENT * caster.damage_multiplier * versatility_multiplier * crit_multiplier * self.spell_damage_modifier * caster_crit_damage_modifier, is_crit
    
    def get_mana_cost(self, caster):
        return self.mana_cost * caster.base_mana * self.mana_cost_modifier
    
    def get_base_mana_cost(self, caster):
        return self.base_mana_cost * caster.base_mana
    
    def start_cooldown(self, caster):
        self.remaining_cooldown = self.calculate_cooldown(caster)
        self.original_cooldown = self.remaining_cooldown
        
    def calculate_cooldown(self, caster):
        if self.hasted_cooldown:
            haste_multiplier = caster.haste_multiplier
            return self.cooldown / haste_multiplier
        else:
            return self.cooldown
        
    def reset_cooldown(self, caster, current_time):
        caster.holy_shock_resets += 1
        
        caster.events.append(f"{format_time(current_time)}: {self.name}'s cooldown was reset")
        if self.current_charges < self.max_charges:
            self.current_charges += 1
            if self.current_charges == self.max_charges:
                self.remaining_cooldown = 0
        else:
            self.remaining_cooldown = 0
            
    def apply_holy_reverberation(self, caster, target, current_time):
        from .auras_buffs import HolyReverberation
        
        if caster.set_bonuses["dragonflight_season_3"] < 2:
            return
        
        new_buff = HolyReverberation(caster)
        if "Holy Reverberation" in target.target_active_buffs:
            if len(target.target_active_buffs["Holy Reverberation"]) >= 6:
                shortest_buff = min(target.target_active_buffs["Holy Reverberation"], key=lambda buff: buff.duration)
                target.target_active_buffs["Holy Reverberation"].remove(shortest_buff)
                update_target_buff_data(caster.target_buff_breakdown, "Holy Reverberation", current_time, "stacks_decremented", target.name, stacks=len(target.target_active_buffs["Holy Reverberation"]))
            target.target_active_buffs["Holy Reverberation"].append(new_buff)
            update_target_buff_data(caster.target_buff_breakdown, "Holy Reverberation", current_time, "stacks_incremented", target.name, stacks=len(target.target_active_buffs["Holy Reverberation"]))
        else:
            target.target_active_buffs["Holy Reverberation"] = [new_buff]
            update_target_buff_data(caster.target_buff_breakdown, new_buff.name, current_time, "applied", target.name, new_buff.duration, new_buff.current_stacks)

        longest_reverberation_duration = max(buff.duration for buff in target.target_active_buffs["Holy Reverberation"])
        caster.events.append(f"{format_time(current_time)}: Holy Reverberation ({len(target.target_active_buffs['Holy Reverberation'])}) applied to {target.name}: {longest_reverberation_duration}s duration")
        
    def try_trigger_rppm_effects(self, caster, targets, current_time):
        from .spells_passives import (
            TouchOfLight, EmbraceOfAkunda, DreamingDevotion, ChirpingRune, LarodarsFieryReverie,
            MagazineOfHealingDarts, BronzedGripWrappings, SacredWeapon, AuthorityOfFieryResolve,
            DivineInspiration, RiteOfAdjurationSpell, ScrapsingersSymphony, GruesomeSyringe
        )
        
        from .auras_buffs import (
            SophicDevotion, EmbraceOfPaku, CoagulatedGenesaurBloodBuff, SustainingAlchemistStoneBuff, 
            AlacritousAlchemistStoneBuff, SeaStarBuff, PipsEmeraldFriendshipBadge, BestFriendsWithPipEmpowered, 
            BestFriendsWithAerwynEmpowered, BestFriendsWithUrctosEmpowered, IdolOfTheSpellWeaverStacks,
            IdolOfTheDreamerStacks, IdolOfTheEarthWarderStacks, IdolOfTheLifeBinderStacks,
            AlliedChestplateOfGenerosity, ElementalLariat, VerdantTether, VerdantConduit,
            PowerOfTheSilverHand, NeltharionsCallToChaos, InspiredByFrostAndEarth, ScreamingBlackDragonscale,
            RashoksMoltenHeart, EmeraldCoachsWhistle, VoiceFromBeyond, BlessingOfAnshe, HarvestersEdict,
            EmpoweringCrystalOfAnubikkaj, UnboundChangeling, FateweavedNeedle,
            AuthorityOfRadiantPower, CouncilsGuile, StormridersFury, StoneboundArtistry, OathswornsTenacity,
            SurekiZealotsInsignia, AraKaraSacbrood
        )
        
        def try_proc_rppm_effect(effect, is_hasted=True, is_heal=False, is_self_buff=False, exclude_mastery=False, is_flat_healing=False, is_other_effect=False):
            # time since last attempt makes it so the number of events happening has very little impact on the number of procs that occur
            proc_occurred = False
            
            caster.time_since_last_rppm_proc[effect.name] = caster.time_since_last_rppm_proc.get(effect.name, 0)
            caster.time_since_last_rppm_proc_attempt[effect.name] = caster.time_since_last_rppm_proc_attempt.get(effect.name, 0)
            
            if is_hasted:
                bad_luck_protection = max(1, 1 + 3 * (caster.time_since_last_rppm_proc[effect.name] * (effect.BASE_PPM * caster.haste_multiplier) / 60 - 1.5))
                effect_proc_chance = bad_luck_protection * ((effect.BASE_PPM * caster.haste_multiplier) / 60) * min(caster.time_since_last_rppm_proc_attempt[effect.name], 10)
            else:
                bad_luck_protection = max(1, 1 + 3 * (caster.time_since_last_rppm_proc[effect.name] * effect.BASE_PPM / 60 - 1.5))
                effect_proc_chance = bad_luck_protection * (effect.BASE_PPM / 60) * min(caster.time_since_last_rppm_proc_attempt[effect.name], 10)
            
            if random.random() < effect_proc_chance:  
                proc_occurred = True   
                caster.time_since_last_rppm_proc[effect.name] = 0
                target = targets[0]
                if is_heal:
                    effect_heal, is_crit = effect.calculate_heal(caster, exclude_mastery=exclude_mastery)
                    target.receive_heal(effect_heal, caster)
                    
                    update_spell_data_heals(caster.ability_breakdown, effect.name, target, effect_heal, is_crit)
                    append_spell_heal_event(caster.events, effect.name, caster, target, effect_heal, current_time, is_crit)
                elif is_other_effect:
                    effect.apply_effect(caster, target, current_time)
                    
                elif is_flat_healing:
                    effect.apply_flat_healing(caster, target, current_time, True)
                 
                if is_self_buff and effect.name in caster.active_auras:
                    if effect.max_stacks > 1:
                        caster.apply_buff_to_self(caster.active_auras[effect.name], current_time, effect.current_stacks, effect.max_stacks)
                    else:
                        effect.remove_effect(caster, current_time)
                        del caster.active_auras[effect.name]
                        caster.apply_buff_to_self(effect, current_time, effect.current_stacks, effect.max_stacks)
                elif is_self_buff:
                    caster.apply_buff_to_self(effect, current_time, effect.current_stacks, effect.max_stacks)
                    
            caster.time_since_last_rppm_proc_attempt[effect.name] = 0
            
            return proc_occurred
        
        # talents
        if caster.is_talent_active("Touch of Light"):        
            touch_of_light = TouchOfLight(caster)        
            try_proc_rppm_effect(touch_of_light, is_heal=True, exclude_mastery=True)
            
        if caster.is_talent_active("Power of the Silver Hand") and (self.name == "Holy Light" or self.name == "Flash of Light" or self.name == "Judgment"):
            power_of_the_silver_hand = PowerOfTheSilverHand()
            try_proc_rppm_effect(power_of_the_silver_hand, is_hasted=False, is_self_buff=True)
            
        if caster.ptr and caster.is_talent_active("Blessing of An'she") and (self.name in ["Eternal Flame", "Dawnlight", "Sun Sear"]):
            blessing_of_anshe = BlessingOfAnshe(caster)
            try_proc_rppm_effect(blessing_of_anshe, is_hasted=False, is_self_buff=True)
            
        if caster.ptr and caster.is_talent_active("Holy Bulwark"):
            sacred_weapon_targets = [target for target in caster.potential_healing_targets if "Sacred Weapon" in target.target_active_buffs]
            if len(sacred_weapon_targets) == 2:
                sacred_weapon_1 = SacredWeapon(caster, 1)
                try_proc_rppm_effect(sacred_weapon_1, is_other_effect=True, is_hasted=False)
                
                sacred_weapon_2 = SacredWeapon(caster, 2)
                try_proc_rppm_effect(sacred_weapon_2, is_other_effect=True, is_hasted=False)
            elif len(sacred_weapon_targets) == 1:
                sacred_weapon_1 = SacredWeapon(caster, 1)
                try_proc_rppm_effect(sacred_weapon_1, is_other_effect=True, is_hasted=False)
        
        if caster.ptr and caster.is_talent_active("Divine Inspiration"):
            divine_inspiration = DivineInspiration(caster)
            try_proc_rppm_effect(divine_inspiration, is_hasted=False, is_other_effect=True)
            
        if caster.ptr and caster.is_talent_active("Rite of Adjuration") and (self.name == "Light of Dawn" or self.name == "Word of Glory"):
            rite_of_adjuration = RiteOfAdjurationSpell(caster)
            try_proc_rppm_effect(rite_of_adjuration, is_hasted=False, is_other_effect=True)
        
        # enchants    
        if "Sophic Devotion" in caster.bonus_enchants:
            sophic_devotion = SophicDevotion()
            try_proc_rppm_effect(sophic_devotion, is_hasted=False, is_self_buff=True)
            
        if "Dreaming Devotion" in caster.bonus_enchants:
            dreaming_devotion = DreamingDevotion(caster)
            try_proc_rppm_effect(dreaming_devotion, is_flat_healing=True)
            
        if caster.ptr and "Authority of Fiery Resolve" in caster.bonus_enchants:
            authority_of_fiery_resolve = AuthorityOfFieryResolve(caster)
            try_proc_rppm_effect(authority_of_fiery_resolve, is_flat_healing=True, is_hasted=False)

        if caster.ptr and "Authority of Radiant Power" in caster.bonus_enchants:
            authority_of_radiant_power = AuthorityOfRadiantPower(caster)
            try_proc_rppm_effect(authority_of_radiant_power, is_self_buff=True, is_hasted=False)
            
        if caster.ptr and "Council's Guile" in caster.bonus_enchants:
            councils_guile = CouncilsGuile(caster)
            try_proc_rppm_effect(councils_guile, is_self_buff=True, is_hasted=False)
            
        if caster.ptr and "Stormrider's Fury" in caster.bonus_enchants:
            stormriders_fury = StormridersFury(caster)
            try_proc_rppm_effect(stormriders_fury, is_self_buff=True, is_hasted=False)
            
        if caster.ptr and "Stonebound Artistry" in caster.bonus_enchants:
            stonebound_artistry = StoneboundArtistry(caster)
            try_proc_rppm_effect(stonebound_artistry, is_self_buff=True, is_hasted=False)

        if caster.ptr and "Oathsworn's Tenacity" in caster.bonus_enchants:
            oathsworns_tenacity = OathswornsTenacity(caster)
            try_proc_rppm_effect(oathsworns_tenacity, is_self_buff=True, is_hasted=False)
            
        if "Incandescent Essence" in caster.bonus_enchants:
            incandescent_essence = LarodarsFieryReverie(caster)
            try_proc_rppm_effect(incandescent_essence, is_flat_healing=True, is_hasted=True)
            
        if "Chirping Rune" in caster.active_auras:
            chirping_rune = ChirpingRune(caster)
            try_proc_rppm_effect(chirping_rune, is_flat_healing=True)
            
        if caster.race == "Zandalari Troll":
            embrace_of_paku = EmbraceOfPaku()
            try_proc_rppm_effect(embrace_of_paku, is_self_buff=True)
            # embrace_of_akunda = EmbraceOfAkunda(caster)
            # try_proc_rppm_effect(embrace_of_akunda, is_heal=True)
            
        if "Fateweaved Mallet" in caster.equipment["main_hand"]["name"]:
            fateweaved_needle = FateweavedNeedle(caster)
            try_proc_rppm_effect(fateweaved_needle, is_hasted=True, is_self_buff=True)
            
        if "Voice of the Silent Star" in caster.equipment["back"]["name"]:
            voice_from_beyond = VoiceFromBeyond(caster)
            if "The Silent Star" not in caster.active_auras:
                try_proc_rppm_effect(voice_from_beyond, is_hasted=False, is_self_buff=True)
                
        if caster.variable_target_counts["Sureki Zealot's Insignia"] > 0:
            sureki_zealots_insignia = SurekiZealotsInsignia(caster)
            try_proc_rppm_effect(sureki_zealots_insignia, is_hasted=False, is_self_buff=True)
            
        # trinkets
        # if "Treacherous Transmitter" in caster.trinkets:
        #     treacherous_transmitter = CrypticInstructions(caster)
        #     try_proc_rppm_effect(treacherous_transmitter, is_hasted=False, is_self_buff=True)
         
        if "Ara-Kara Sacbrood" in caster.trinkets:
            ara_kara_sacbrood = AraKaraSacbrood(caster)
            try_proc_rppm_effect(ara_kara_sacbrood, is_hasted=False, is_self_buff=True)
        
        if "Unbound Changeling" in caster.trinkets:
            unbound_changeling = UnboundChangeling(caster)
            try_proc_rppm_effect(unbound_changeling, is_self_buff=True)
            
        if "Gruesome Syringe" in caster.trinkets:
            gruesome_syringe = GruesomeSyringe(caster)
            try_proc_rppm_effect(gruesome_syringe, is_hasted=False, is_flat_healing=True)
        
        if "Scrapsinger's Symphony" in caster.trinkets:
            scrapsingers_symphony = ScrapsingersSymphony(caster)
            try_proc_rppm_effect(scrapsingers_symphony, is_hasted=True, is_flat_healing=True)
        
        if "Harvester's Edict" in caster.trinkets and self.name in ["Judgment", "Crusader Strike", "Consecration", "Hammer of Wrath"]:
            harvesters_edict = HarvestersEdict(caster)
            try_proc_rppm_effect(harvesters_edict, is_hasted=True, is_self_buff=True)
            
        if "Empowering Crystal of Anub'ikkaj" in caster.trinkets:
            empowering_crystal_of_anubikkaj = EmpoweringCrystalOfAnubikkaj(caster)
            try_proc_rppm_effect(empowering_crystal_of_anubikkaj, is_hasted=False, is_self_buff=True)
        
        if "Emerald Coach's Whistle" in caster.trinkets:
            emerald_coachs_whistle = EmeraldCoachsWhistle(caster)
            try_proc_rppm_effect(emerald_coachs_whistle, is_hasted=False, is_self_buff=True)
        
        if "Rashok's Molten Heart" in caster.trinkets:
            rashoks_molten_heart = RashoksMoltenHeart(caster)
            try_proc_rppm_effect(rashoks_molten_heart, is_hasted=False, is_self_buff=True)
        
        if "Screaming Black Dragonscale" in caster.trinkets:
            screaming_black_dragonscale = ScreamingBlackDragonscale(caster)
            try_proc_rppm_effect(screaming_black_dragonscale, is_hasted=False, is_self_buff=True)
        
        if "Whispering Incarnate Icon" in caster.trinkets:
            whispering_incarnate_icon = InspiredByFrostAndEarth(caster)
            try_proc_rppm_effect(whispering_incarnate_icon, is_hasted=False, is_self_buff=True)
        
        if "Neltharion's Call to Chaos" in caster.trinkets:
            neltharions_call_to_chaos = NeltharionsCallToChaos(caster)
            if self.name in ["Light of Dawn", "Consecration", "Light's Hammer"]:
                try_proc_rppm_effect(neltharions_call_to_chaos, is_hasted=False, is_self_buff=True)
        
        if "Coagulated Genesaur Blood" in caster.trinkets:
            coagulated_genesaur_blood = CoagulatedGenesaurBloodBuff(caster)
            try_proc_rppm_effect(coagulated_genesaur_blood, is_hasted=False, is_self_buff=True)
            
        if "Sea Star" in caster.trinkets:
            sea_star = SeaStarBuff(caster)
            try_proc_rppm_effect(sea_star, is_hasted=False, is_self_buff=True)
            
        if "Sustaining Alchemist Stone" in caster.trinkets:
            sustaining_alchemist_stone = SustainingAlchemistStoneBuff(caster)
            try_proc_rppm_effect(sustaining_alchemist_stone, is_self_buff=True)
            
        if "Alacritous Alchemist Stone" in caster.trinkets:
            alacritous_alchemist_stone = AlacritousAlchemistStoneBuff(caster)
            try_proc_rppm_effect(alacritous_alchemist_stone, is_self_buff=True)
            
        if "Pip's Emerald Friendship Badge" in caster.trinkets:
            pips_emerald_friendship_badge = PipsEmeraldFriendshipBadge(caster)
            pips_proc = try_proc_rppm_effect(pips_emerald_friendship_badge, is_hasted=False, is_self_buff=True)
            
            if pips_proc:
                new_pips_proc = random.choice([BestFriendsWithPipEmpowered(caster), BestFriendsWithAerwynEmpowered(caster), BestFriendsWithUrctosEmpowered(caster)])
                # remove permanent buff
                if "Best Friends with Pip" in caster.active_auras:
                    caster.remove_or_decrement_buff_on_self(caster.active_auras["Best Friends with Pip"], current_time)
                elif "Best Friends with Aerwyn" in caster.active_auras:
                    caster.remove_or_decrement_buff_on_self(caster.active_auras["Best Friends with Aerwyn"], current_time)
                elif "Best Friends with Urctos" in caster.active_auras:
                    caster.remove_or_decrement_buff_on_self(caster.active_auras["Best Friends with Urctos"], current_time)
                    
                # if it procs during an existing empower, remove the existing empower
                if "Best Friends with Pip Empowered" in caster.active_auras:
                    caster.remove_or_decrement_buff_on_self(caster.active_auras["Best Friends with Pip Empowered"], current_time, replaced=True)    
                elif "Best Friends with Aerwyn Empowered" in caster.active_auras:
                    caster.remove_or_decrement_buff_on_self(caster.active_auras["Best Friends with Aerwyn Empowered"], current_time, replaced=True)
                elif "Best Friends with Urctos Empowered" in caster.active_auras:
                    caster.remove_or_decrement_buff_on_self(caster.active_auras["Best Friends with Urctos Empowered"], current_time, replaced=True)
                
                caster.apply_buff_to_self(new_pips_proc, current_time)
                
        if "Idol of the Dreamer" in caster.trinkets:
            idol_of_the_dreamer = IdolOfTheDreamerStacks(caster)
            if "Idol of the Dreamer Empowered" not in caster.active_auras:
                try_proc_rppm_effect(idol_of_the_dreamer, is_hasted=False, is_self_buff=True)
                
        if "Idol of the Life-Binder" in caster.trinkets:
            idol_of_the_lifebinder = IdolOfTheLifeBinderStacks(caster)
            if "Idol of the Life-Binder Empowered" not in caster.active_auras:
                try_proc_rppm_effect(idol_of_the_lifebinder, is_hasted=False, is_self_buff=True)
                
        if "Idol of the Earth-Warder" in caster.trinkets:
            idol_of_the_earthwarder = IdolOfTheEarthWarderStacks(caster)
            if "Idol of the Earth-Warder Empowered" not in caster.active_auras:
                try_proc_rppm_effect(idol_of_the_earthwarder, is_hasted=False, is_self_buff=True)
                
        if "Idol of the Spell-Weaver" in caster.trinkets:
            idol_of_the_spellweaver = IdolOfTheSpellWeaverStacks(caster)
            if "Idol of the Spell-Weaver Empowered" not in caster.active_auras:
                try_proc_rppm_effect(idol_of_the_spellweaver, is_hasted=False, is_self_buff=True)
        
        # embellishments   
        if "Elemental Lariat" in caster.embellishments:
            elemental_lariat = ElementalLariat(caster)
            if "Elemental Lariat" not in caster.active_auras:
                try_proc_rppm_effect(elemental_lariat, is_hasted=False, is_self_buff=True)
            
        if "Allied Chestplate of Generosity" in caster.embellishments:
            allied_chestplate_of_generosity = AlliedChestplateOfGenerosity(caster)
            try_proc_rppm_effect(allied_chestplate_of_generosity, is_hasted=False, is_self_buff=True)
            
        if "Verdant Tether" in caster.embellishments:
            verdant_tether = VerdantTether(caster)
            try_proc_rppm_effect(verdant_tether, is_hasted=False, is_self_buff=True)
            
        if "Verdant Conduit" in caster.embellishments:
            verdant_conduit = VerdantConduit(caster)
            if "Verdant Conduit" not in caster.active_auras:
                try_proc_rppm_effect(verdant_conduit, is_hasted=False, is_self_buff=True)
                
        if "Magazine of Healing Darts" in caster.embellishments:
            healing_dart = MagazineOfHealingDarts(caster)
            try_proc_rppm_effect(healing_dart, is_flat_healing=True)
            
        if "Bronzed Grip Wrappings" in caster.embellishments:
            bronzed_grip_wrappings = BronzedGripWrappings(caster)
            try_proc_rppm_effect(bronzed_grip_wrappings, is_flat_healing=True)
                
    def try_trigger_conditional_effects(self, caster, targets, current_time):
        from .spells_passives import EchoingTyrstoneProc, BlossomOfAmirdrassilProc
        from .trinkets import EchoingTyrstone
        
        if caster.is_trinket_equipped("Echoing Tyrstone"):
            echoing_tyrstone_cast = EchoingTyrstone(caster)
            echoing_tyrstone_proc = EchoingTyrstoneProc(caster)
            
            caster.conditional_effect_cooldowns[echoing_tyrstone_proc.name] = caster.conditional_effect_cooldowns.get(echoing_tyrstone_proc.name, 0)
            
            if current_time >= echoing_tyrstone_cast.tyrstone_end_time + echoing_tyrstone_proc.AVERAGE_TIME_TO_PROC and caster.conditional_effect_cooldowns[echoing_tyrstone_proc.name] <= 0:
                caster.conditional_effect_cooldowns[echoing_tyrstone_proc.name] = echoing_tyrstone_cast.BASE_COOLDOWN
                echoing_tyrstone_proc.trigger_proc(caster, targets, current_time)
                
        if caster.is_trinket_equipped("Blossom of Amirdrassil"):
            blossom_proc = BlossomOfAmirdrassilProc(caster)
            
            caster.conditional_effect_cooldowns[blossom_proc.name] = caster.conditional_effect_cooldowns.get(blossom_proc.name, 0)
            if current_time >= blossom_proc.AVERAGE_TIME_TO_PROC and caster.conditional_effect_cooldowns[blossom_proc.name] <= 0:
                caster.conditional_effect_cooldowns[blossom_proc.name] = blossom_proc.BASE_COOLDOWN
                blossom_proc.trigger_proc(caster, targets, current_time)
                          
    def collect_priority_breakdown_data(self, caster, targets=None, exclude_target_auras=False):
        # add auras to dictionaries and check current spell cooldownsfor display in priority list example
        self_auras = defaultdict(dict)
        for aura in caster.active_auras.values():
            self_auras[aura.name] = {"duration": caster.active_auras[aura.name].duration, "stacks": caster.active_auras[aura.name].current_stacks, "applied_duration": caster.active_auras[aura.name].base_duration}
         
        target_auras = defaultdict(dict)  
        if not exclude_target_auras:
            # remove this line to add data for multi target spells
            if self.healing_target_count == 1:
                for target in targets:
                    for auras in target.target_active_buffs.values():
                        for aura in auras:
                            target_auras[target.name][aura.name] = {"duration": aura.duration, "stacks": aura.current_stacks, "applied_duration": aura.applied_duration}
        
        # count the auras active across all targets
        total_target_aura_counts = defaultdict(dict)
        for target in caster.potential_healing_targets:
            for aura in target.target_active_buffs:
                total_target_aura_counts[aura] = total_target_aura_counts.get(aura, 0) + 1
        
        # check cooldowns and add to priority breakdown
        spell_cooldowns = caster.check_cooldowns()
        
        # check stats
        stats = caster.check_stats()
        
        return self_auras, target_auras, total_target_aura_counts, spell_cooldowns, stats
   
        
class Wait(Spell):
# waits until next gcd

    def __init__(self):
        super().__init__("Wait")