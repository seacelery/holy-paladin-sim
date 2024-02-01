import random

from .auras import Buff
from ..utils.misc_functions import append_spell_heal_event, format_time, update_mana_gained, update_self_buff_data, update_spell_data_heals, calculate_beacon_healing, update_spell_data_beacon_heals, append_spell_beacon_event
from ..utils.beacon_transfer_rates import beacon_transfer_rates_single_beacon, beacon_transfer_rates_double_beacon


class HoT(Buff):
    
    def __init__(self, name, duration, base_duration, base_tick_interval, initial_haste_multiplier, current_stacks=1, max_stacks=1, hasted=True):
        super().__init__(name, duration, base_duration, current_stacks=current_stacks, max_stacks=max_stacks) 
        self.base_tick_interval = base_tick_interval 
        self.time_until_next_tick = base_tick_interval
        self.total_ticks = 0
        self.previous_haste_multiplier = initial_haste_multiplier
        self.previous_tick_time = 0
        self.hasted = hasted
        
    def add_stack(self, new_buff_instance):
        self.buff_instances.append(new_buff_instance)
        
    def process_tick(self, caster, target, current_time, buff_instances, is_partial_tick=False):
        if is_partial_tick and not self.hasted:
            return
        
        total_heal_value, is_crit = self.calculate_tick_healing(caster) 
        total_heal_value *= len(buff_instances)
        
        if is_crit:
            total_heal_value *= 2
        
        if is_partial_tick:
            total_heal_value *= (current_time - self.previous_tick_time) / (self.base_tick_interval / caster.haste_multiplier)
            
        target.receive_heal(total_heal_value)
        
        caster.handle_beacon_healing(self.name, target, total_heal_value, current_time)
        
        if is_crit and self.name == "Holy Reverberation":
            caster.events.append(f"{format_time(current_time)}: Holy Reverberation crit healed {target.name} for {round(total_heal_value)}")
        elif self.name == "Holy Reverberation":
            caster.events.append(f"{format_time(current_time)}: Holy Reverberation healed {target.name} for {round(total_heal_value)}")
            
        self.total_ticks += 1 if not is_partial_tick else self.time_until_next_tick / self.base_tick_interval
        
        update_spell_data_heals(caster.ability_breakdown, self.name, target, total_heal_value, is_crit)
        
        
    def calculate_tick_healing(self, caster):
        # spell_power = caster.stats.ratings["intellect"]
        spell_power = 9340
        
        total_healing = spell_power * self.SPELL_POWER_COEFFICIENT * caster.healing_multiplier
        
        mastery_multiplier = 1 + (caster.mastery_multiplier - 1) * caster.mastery_effectiveness
        versatility_multiplier = caster.versatility_multiplier
        total_healing *= mastery_multiplier * versatility_multiplier

        if self.hasted:
            number_of_ticks = self.base_duration / (self.base_tick_interval / caster.haste_multiplier)
            if number_of_ticks > 1:
                total_healing *= caster.haste_multiplier
            healing_per_tick = total_healing / number_of_ticks
        else:
            number_of_ticks = self.base_duration / self.base_tick_interval
            healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        crit_chance = caster.crit
        random_num = random.random() * 100
        if random_num <= crit_chance:
            is_crit = True

        return healing_per_tick, is_crit


# class GiftOfTheNaaruBuff(HoT):
    
#     SPELL_POWER_COEFFICIENT = 0
    
#     def __init__(self, caster):
#         super().__init__("Gift of the Naaru", 5, base_duration=5, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier)
#         self.time_until_next_tick = self.base_tick_interval / caster.haste_multiplier

class GiftOfTheNaaruBuff(HoT):
    
    def __init__(self, caster):
        super().__init__("Gift of the Naaru", 5, base_duration=5, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        self.time_until_next_tick = self.base_tick_interval
        
    def calculate_tick_healing(self, caster):
        total_healing = caster.max_health * 0.2
        
        number_of_ticks = self.base_duration / self.base_tick_interval
        healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        crit_chance = caster.crit
        random_num = random.random() * 100
        if random_num <= crit_chance:
            is_crit = True

        return healing_per_tick, is_crit
        
class HolyReverberation(HoT):
    
    SPELL_POWER_COEFFICIENT = 1.08 * 0.8
    
    def __init__(self, caster):
        super().__init__("Holy Reverberation", 8, base_duration=8, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, current_stacks=1, max_stacks=6) 
        self.time_until_next_tick = self.base_tick_interval / caster.haste_multiplier
    
    
# self buffs   


class AvengingWrathBuff(Buff):
    
    def __init__(self):
        super().__init__("Avenging Wrath", 20, base_duration=20)
        
    def apply_effect(self, caster, current_time=None):
        if "Avenging Wrath (Awakening)" in caster.active_auras:
            caster.active_auras["Avenging Wrath (Awakening)"].remove_effect(caster)
            del caster.active_auras["Avenging Wrath (Awakening)"]   
            update_self_buff_data(caster.self_buff_breakdown, "Avenging Wrath (Awakening)", current_time, "expired")      
        
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.crit += 15
        caster.healing_multiplier *= 1.15
        caster.damage_multiplier *= 1.15
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.crit -= 15
        caster.healing_multiplier /= 1.15
        caster.damage_multiplier /= 1.15
       
       
class AvengingWrathAwakening(Buff):
     
    def __init__(self):
        super().__init__("Avenging Wrath (Awakening)", 12, base_duration=12)
        
    def apply_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.crit += 15
        caster.healing_multiplier *= 1.15
        caster.damage_multiplier *= 1.15
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.crit -= 15
        caster.healing_multiplier /= 1.15
        caster.damage_multiplier /= 1.15
        
class DivineFavorBuff(Buff):
    
    def __init__(self):
        super().__init__("Divine Favor", 10000)
        
    def apply_effect(self, caster, current_time=None):
        # for aura in caster.active_auras:
        #     print(current_time, aura, caster.active_auras[aura].duration, caster.active_auras[aura].current_stacks)
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].spell_healing_modifier *= 1.6
            caster.abilities["Holy Light"].cast_time_modifier *= 0.7
            caster.abilities["Holy Light"].mana_cost_modifier *= 0.5
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].spell_healing_modifier *= 1.6
            caster.abilities["Flash of Light"].cast_time_modifier *= 0.7
            caster.abilities["Flash of Light"].mana_cost_modifier *= 0.5
            
    def remove_effect(self, caster, current_time=None):
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].spell_healing_modifier /= 1.6
            caster.abilities["Holy Light"].cast_time_modifier /= 0.7
            caster.abilities["Holy Light"].mana_cost_modifier /= 0.5
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].spell_healing_modifier /= 1.6
            caster.abilities["Flash of Light"].cast_time_modifier /= 0.7
            caster.abilities["Flash of Light"].mana_cost_modifier /= 0.5
        
        
class InfusionOfLight(Buff):
    
    def __init__(self, caster):
        super().__init__("Infusion of Light", 15, base_duration=15)
        if caster.is_talent_active("Inflorescence of the Sunwell"):
            self.current_stacks = 2
            self.max_stacks = 2
        
    def apply_effect(self, caster, current_time=None):
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].mana_cost_modifier *= 0
        
    def remove_effect(self, caster, current_time=None):
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].mana_cost_modifier = 1
            if "Divine Favor" in caster.active_auras:
                caster.abilities["Flash of Light"].mana_cost_modifier *= 0.7
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].holy_power_gain = 1


class DivineResonance(Buff):
    
    def __init__(self):
        super().__init__("Divine Resonance", 15, base_duration=15)
        self.last_holy_shock_time = 0
        
    def apply_effect(self, caster, current_time=None):
        self.last_holy_shock_time = 0
    
    def increment_divine_resonance(self, caster, current_time, tick_rate):
        self.last_holy_shock_time += tick_rate
        if self.last_holy_shock_time >= 5 - tick_rate - 0.01:
            self.trigger_divine_resonance_holy_shock(caster, current_time)
            self.last_holy_shock_time = 0
    
    def trigger_divine_resonance_holy_shock(self, caster, current_time):
        from .spells_healing import DivineResonanceHolyShock
        
        glimmer_targets = [glimmer_target for glimmer_target in caster.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        non_glimmer_targets = [glimmer_target for glimmer_target in caster.potential_healing_targets if "Glimmer of Light" not in glimmer_target.target_active_buffs]
        non_glimmer_non_beacon_targets = [t for t in non_glimmer_targets if t not in caster.beacon_targets] 
        target = [random.choice(non_glimmer_non_beacon_targets)]
        # target = [random.choice([t for t in caster.potential_healing_targets if t.name == "target18"])]
        DivineResonanceHolyShock(caster).cast_healing_spell(caster, target, current_time, is_heal=True, glimmer_targets=glimmer_targets)
        
            
class RisingSunlight(Buff):
    
    def __init__(self):
        super().__init__("Rising Sunlight", 30, base_duration=30, current_stacks=3, max_stacks=3)
       
        
class FirstLight(Buff):
    
    # casting Daybreak increases haste by 25% for 6 seconds
    def __init__(self):
        super().__init__("First Light", 6, base_duration=6)
        
    def apply_effect(self, caster, current_time=None):
        caster.haste_multiplier *= 1.25
        caster.update_hasted_cooldowns_with_haste_changes()
    
    def remove_effect(self, caster, current_time=None):
        caster.haste_multiplier /= 1.25
        caster.update_hasted_cooldowns_with_haste_changes()
        
        
class AwakeningStacks(Buff):
    
    def __init__(self):
        super().__init__("Awakening", 60, base_duration=60, current_stacks=1, max_stacks=12, base_duration=60)
       
        
class AwakeningTrigger(Buff):
    
    def __init__(self):
        super().__init__("Awakening READY!!!!!!", 30, base_duration=30)
        
        
class TyrsDeliveranceSelfBuff(Buff):
    
    def __init__(self):
        super().__init__("Tyr's Deliverance (self)", 20, base_duration=20)
        self.last_tyr_tick_time = 0
        self.base_tick_interval = 1
        
    def apply_effect(self, caster, current_time=None):
        self.last_tyr_tick_time = 0
        caster.tyrs_deliverance_extended_by = 0
    
    def increment_tyrs_deliverance(self, caster, current_time, tick_rate):
        self.last_tyr_tick_time += tick_rate
        if self.last_tyr_tick_time >= self.base_tick_interval / caster.haste_multiplier:
            self.trigger_tyrs_deliverance_tick(caster, current_time)
            self.last_tyr_tick_time = 0
    
    def trigger_tyrs_deliverance_tick(self, caster, current_time):
        from .spells_auras import TyrsDeliveranceHeal
        
        non_tyrs_targets = [target for target in caster.potential_healing_targets if "Tyr's Deliverance (target)" not in target.target_active_buffs]
        if len(non_tyrs_targets) > 0:
            target = [random.choice(non_tyrs_targets)]
        else:
            target = [random.choice(caster.potential_healing_targets)]
        # target = [random.choice([t for t in caster.potential_healing_targets if t.name == "target18"])]
        TyrsDeliveranceHeal(caster).cast_healing_spell(caster, target, current_time, is_heal=True)
        
    def trigger_partial_tick(self, caster, current_time):
        from .spells_auras import TyrsDeliveranceHeal
        
        non_tyrs_targets = [target for target in caster.potential_healing_targets if "Tyr's Deliverance (target)" not in target.target_active_buffs]
        target = [random.choice(non_tyrs_targets)]
        # target = [random.choice([t for t in caster.potential_healing_targets if t.name == "target18"])]
        spell = TyrsDeliveranceHeal(caster)
        hasted_tick_interval = self.base_tick_interval / caster.haste_multiplier

        # with a low tick rate if it lines up perfectly it can try to divide by 0
        spell.spell_healing_modifier *= (hasted_tick_interval - (hasted_tick_interval - self.last_tyr_tick_time - 0.0001)) / hasted_tick_interval
        spell.cast_healing_spell(caster, target, current_time, is_heal=True)
        spell.spell_healing_modifier /= (hasted_tick_interval - (hasted_tick_interval - self.last_tyr_tick_time  - 0.0001)) / hasted_tick_interval
        
        
class DivinePurpose(Buff):
    
    def __init__(self):
        super().__init__("Divine Purpose", 12, base_duration=12)
        
        
class BlessingOfDawn(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Dawn", 20, base_duration=20, current_stacks=1, max_stacks=2)
        
        
class BlessingOfDusk(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Dusk", 10, base_duration=10)
      
        
class SophicDevotion(Buff):
    
    BASE_PPM = 1
    
    def __init__(self):
        super().__init__("Sophic Devotion", 15, base_duration=15)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(932)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(932)
 
 
# target buffs   
class BeaconOfLightBuff(Buff):
    
    def __init__(self):
        super().__init__("Beacon of Light", 10000, base_duration=10000)
        
             
class GlimmerOfLightBuff(Buff):
    
    def __init__(self):
        super().__init__("Glimmer of Light", 30, base_duration=30)
    
    
class BlessingOfFreedomBuff(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Freedom", 8, base_duration=8)
        
        
class TyrsDeliveranceTargetBuff(Buff):
    
    def __init__(self):
        super().__init__("Tyr's Deliverance (target)", 12, base_duration=12)
        
        
class BlessingOfSummer(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Summer", 30, base_duration=30)
        
        
class BlessingOfAutumn(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Autumn", 30, base_duration=30)
        
        
class BlessingOfWinter(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Winter", 30, base_duration=30)
        self.last_holy_shock_time = 0
        
    def apply_effect(self, caster, current_time=None):
        self.last_winter_tick_time = 0
        self.mana_gained = 0
    
    def increment_blessing_of_winter(self, caster, current_time, tick_rate):       
        self.last_winter_tick_time += tick_rate
        if self.last_winter_tick_time >= 2.94:
            winter_mana_gain = caster.max_mana * 0.01
            caster.mana += winter_mana_gain
            update_mana_gained(caster.ability_breakdown, "Blessing of Winter", winter_mana_gain)
            self.mana_gained += caster.max_mana * 0.01
            
            self.last_winter_tick_time = 0
            
        if caster.active_auras["Blessing of Winter"].duration < 0.01:
            caster.events.append(f"{format_time(current_time)}: {caster.name} gained {round(self.mana_gained)} mana from Blessing of Winter")
    
    
class BlessingOfSpring(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Spring", 30, base_duration=30)
        
    def apply_effect(self, caster, current_time=None):
        caster.healing_multiplier *= 1.15
        
    def remove_effect(self, caster, current_time=None):
        caster.healing_multiplier /= 1.15
        

class EmbraceOfPaku(Buff):
    
    BASE_PPM = 1
    
    def __init__(self):
        super().__init__("Embrace of Pa'ku", 12, base_duration=12)
        
    def apply_effect(self, caster, current_time=None):
        caster.crit += 4
        
    def remove_effect(self, caster, current_time=None):
        caster.crit -= 4
        

class FirebloodBuff(Buff):
    
    # TODO add an option for removing debuffs
    def __init__(self):
        super().__init__("Fireblood", 8, base_duration=8)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(875)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(875)
        
        
class TimeWarp(Buff):
    
    def __init__(self):
        super().__init__("Time Warp", 40, base_duration=40)
        
    def apply_effect(self, caster, current_time=None):
        caster.haste_multiplier *= 1.3
        caster.update_hasted_cooldowns_with_haste_changes()
    
    def remove_effect(self, caster, current_time=None):
        caster.haste_multiplier /= 1.3
        caster.update_hasted_cooldowns_with_haste_changes()
        
        
# consumables
class ElementalPotionOfUltimatePowerBuff(Buff):
    
    def __init__(self):
        super().__init__("Elemental Potion of Ultimate Power", 30, base_duration=30)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(886)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(886)
        

class PhialOfTepidVersatility(Buff):
    
    def __init__(self):
        super().__init__("Phial of Tepid Versatility", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.base_versatility += 745 / 205
        
    def remove_effect(self, caster, current_time=None):
        caster.base_versatility -= 745 / 205
        
        
def apply_elemental_chaos_aura(caster, current_time):
        elemental_chaos_auras = [
            ElementalChaosAir,
            ElementalChaosEarth, 
            ElementalChaosFire,
            ElementalChaosFrost
        ]
        
        existing_buff = None
        for aura in caster.active_auras.values():
            if isinstance(aura, tuple(elemental_chaos_auras)):
                existing_buff = aura
                break
            
        chosen_aura_class = random.choice(elemental_chaos_auras)

        if existing_buff and isinstance(existing_buff, chosen_aura_class):
            existing_buff.reapply_self(caster, current_time)          
        else:
            chosen_aura = chosen_aura_class()
            caster.apply_buff_to_self(chosen_aura, current_time)
        
class PhialOfElementalChaos(Buff):
    
    def __init__(self):
        super().__init__("Phial of Elemental Chaos", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        apply_elemental_chaos_aura(caster, 0)
        
    def remove_effect(self, caster, current_time=None):
        pass
        
        
class ElementalChaosAir(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Air", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.base_haste += caster.get_percent_from_stat_rating("Haste", 652)
        
    def remove_effect(self, caster, current_time):
        caster.base_haste -= caster.get_percent_from_stat_rating("Haste", 652)
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        
class ElementalChaosFire(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Fire", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.base_crit += caster.get_percent_from_stat_rating("Crit", 652)
        caster.crit_damage_modifier += 0.02
        
    def remove_effect(self, caster, current_time):
        caster.base_crit -= caster.get_percent_from_stat_rating("Crit", 652)
        caster.crit_damage_modifier -= 0.02
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        

class ElementalChaosFrost(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Frost", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.base_versatility += caster.get_percent_from_stat_rating("Versatility", 652)
        caster.crit_healing_modifier += 0.02
        
    def remove_effect(self, caster, current_time):
        caster.base_versatility -= caster.get_percent_from_stat_rating("Versatility", 652)
        caster.crit_healing_modifier -= 0.02
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        

class ElementalChaosEarth(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Earth", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.base_mastery += caster.get_percent_from_stat_rating("Mastery", 652)
        
    def remove_effect(self, caster, current_time):
        caster.base_mastery -= caster.get_percent_from_stat_rating("Mastery", 652)
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)