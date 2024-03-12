import random
import re

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
            
        target.receive_heal(total_heal_value, caster)
        
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
            caster.flat_crit += 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier *= 1.15
        caster.damage_multiplier *= 1.15
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.flat_crit -= 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier /= 1.15
        caster.damage_multiplier /= 1.15
       
       
class AvengingWrathAwakening(Buff):
     
    def __init__(self):
        super().__init__("Avenging Wrath (Awakening)", 12, base_duration=12)
        
    def apply_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.flat_crit += 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier *= 1.15
        caster.damage_multiplier *= 1.15
        
    def remove_effect(self, caster, current_time=None):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.flat_crit -= 15
            caster.update_stat("crit", 0)
        caster.healing_multiplier /= 1.15
        caster.damage_multiplier /= 1.15
        
class DivineFavorBuff(Buff):
    
    def __init__(self):
        super().__init__("Divine Favor", 10000)
        
    def apply_effect(self, caster, current_time=None):
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
        self.last_winter_tick_time = 0
        
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
        caster.flat_crit += 4
        caster.update_stat("crit", 0)
        
    def remove_effect(self, caster, current_time=None):
        caster.flat_crit -= 4
        caster.update_stat("crit", 0)
        

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
        caster.update_stat_with_multiplicative_percentage("haste", 30, True)
    
    def remove_effect(self, caster, current_time=None):
        caster.update_stat_with_multiplicative_percentage("haste", 30, False)
        
        
## consumables
# potions
class ElementalPotionOfUltimatePowerBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Elemental Potion of Ultimate Power", 30, base_duration=30)
        if "Potion Absorption Inhibitor" in caster.active_auras:
            print("a", caster.active_auras["Potion Absorption Inhibitor"].current_stacks)
            self.duration *= 1 + (0.5 * caster.active_auras["Potion Absorption Inhibitor"].current_stacks)
            self.base_duration *= 1 + (0.5 * caster.active_auras["Potion Absorption Inhibitor"].current_stacks)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(886)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(886)
        

# phials
class PhialOfTepidVersatility(Buff):
    
    def __init__(self):
        super().__init__("Phial of Tepid Versatility", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 745)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -745)
        
        
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
        # print(f"{chosen_aura_class} chosen, {current_time}")

        if existing_buff and isinstance(existing_buff, chosen_aura_class):
            existing_buff.reapply_self(caster, current_time)          
        else:
            chosen_aura = chosen_aura_class()
            # print("APPLYING ELEMENTAL CHAOS AURA")
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
        caster.update_stat("haste", 652)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -652)
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        
        
class ElementalChaosFire(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Fire", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 652)
        caster.crit_damage_modifier += 0.02
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("crit", -652)
        caster.crit_damage_modifier -= 0.02
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)


class ElementalChaosFrost(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Frost", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 652)
        caster.crit_healing_modifier += 0.02
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("versatility", -652)
        caster.crit_healing_modifier -= 0.02
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
        

class ElementalChaosEarth(Buff):
    
    def __init__(self):
        super().__init__("Elemental Chaos: Earth", 60, base_duration=60)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 652)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("mastery", -652)
        apply_elemental_chaos_aura(caster, current_time)
        
    def reapply_self(self, caster, current_time):
        new_buff = self.__class__()
        caster.apply_buff_to_self(new_buff, current_time, reapply=True)
    

# food
class GrandBanquetOfTheKaluakFood(Buff):
    
    def __init__(self):
        super().__init__("Grand Banquet of the Kalu'ak", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(75)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(75)


class TimelyDemiseFood(Buff):
    
    def __init__(self):
        super().__init__("Timely Demise", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 105)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -105)

        
        
class FiletOfFangsFood(Buff):
    
    def __init__(self):
        super().__init__("Filet of Fangs", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 105)

        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -105)
        
        
class SeamothSurpriseFood(Buff):
    
    def __init__(self):
        super().__init__("Seamoth Surprise", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 105)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -105)


class SaltBakedFishcakeFood(Buff):
    
    def __init__(self):
        super().__init__("Salt-Baked Fishcake", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 105)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -105)
        
        
class FeistyFishSticksFood(Buff):
    
    def __init__(self):
        super().__init__("Feisty Fish Sticks", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 67)
        caster.update_stat("haste", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -67)
        caster.update_stat("haste", -67)
        

class AromaticSeafoodPlatterFood(Buff):
    
    def __init__(self):
        super().__init__("Aromatic Seafood Platter", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", 67)
        caster.update_stat("haste", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("versatility", -67)
        caster.update_stat("haste", -67)


class SizzlingSeafoodMedleyFood(Buff):
    
    def __init__(self):
        super().__init__("Sizzling Seafood Medley", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 67)
        caster.update_stat("haste", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -67)
        caster.update_stat("haste", -67)
        
        
class RevengeServedColdFood(Buff):
    
    def __init__(self):
        super().__init__("Revenge, Served Cold", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 67)
        caster.update_stat("versatility", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -67)
        caster.update_stat("versatility", -67)
        
        
class ThousandboneTongueslicerFood(Buff):
    
    def __init__(self):
        super().__init__("Thousandbone Tongueslicer", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 67)
        caster.update_stat("crit", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -67)
        caster.update_stat("crit", -67)


class GreatCeruleanSeaFood(Buff):
    
    def __init__(self):
        super().__init__("Great Cerulean Sea", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 67)
        caster.update_stat("versatility", 67)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -67)
        caster.update_stat("versatility", -67)
        
        
# weapon imbues
class BuzzingRune(Buff):
    
    def __init__(self):
        super().__init__("Buzzing Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", 310)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -310)


class ChirpingRune(Buff):
    
    def __init__(self):
        super().__init__("Chirping Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
        

class HowlingRune(Buff):
    
    def __init__(self):
        super().__init__("Howling Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", 310)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -310)
        

class HissingRune(Buff):
    
    def __init__(self):
        super().__init__("Hissing Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", 310)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -310)
        
        
# augment runes
class DraconicAugmentRune(Buff):
    
    def __init__(self):
        super().__init__("Draconic Augment Rune", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power += caster.get_effective_spell_power(87)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(87)
        
        
# RAID BUFFS
class ArcaneIntellect(Buff):
    
    def __init__(self):
        super().__init__("Arcane Intellect", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.spell_power *= 1.05
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power /= 1.05
        
        
class MarkOfTheWild(Buff):
    
    def __init__(self):
        super().__init__("Mark of the Wild", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        caster.flat_versatility += 3
        caster.update_stat("versatility", 0)
        
    def remove_effect(self, caster, current_time=None):
        caster.flat_versatility -= 3
        caster.update_stat("versatility", 0)
        

class CloseToHeart(Buff):
    
    def __init__(self):
        super().__init__("Close to Heart", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    
    
class RetributionAura(Buff):
    
    def __init__(self):
        super().__init__("Retribution Aura", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
        
        
# EXTERNAL BUFFS
class SourceOfMagic(Buff):
    
    def __init__(self):
        super().__init__("Source of Magic", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class PowerInfusion(Buff):
    def __init__(self):
        super().__init__("Power Infusion", 15, base_duration=15)
        
    def apply_effect(self, caster, current_time=None):
        caster.flat_haste += 20
        caster.update_stat("haste", 0)
        caster.update_hasted_cooldowns_with_haste_changes()
    
    def remove_effect(self, caster, current_time=None):
        caster.flat_haste -= 20
        caster.update_stat("haste", 0)
        caster.update_hasted_cooldowns_with_haste_changes()
        
        
class Innervate(Buff):
    def __init__(self):
        super().__init__("Innervate", 8, base_duration=8)
        
    def apply_effect(self, caster, current_time=None):
        caster.innervate_active = True
    
    def remove_effect(self, caster, current_time=None):
        caster.innervate_active = False
        

# trinkets
class MirrorOfFracturedTomorrowsBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Mirror of Fractured Tomorrows", 20, base_duration=20)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # flat healing
        self.trinket_first_value = trinket_values[0]
        # highest secondary stat rating
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):  
        from .spells_passives import RestorativeSands
        target = random.choice(caster.potential_healing_targets)
        restorative_sands_heal, restorative_sands_crit = RestorativeSands(caster).calculate_heal(caster)
        restorative_sands_heal = self.trinket_first_value * caster.versatility_multiplier
        if restorative_sands_crit:
            restorative_sands_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
            
        
        # average 4 heals
        for i in range(4):
            target.receive_heal(restorative_sands_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Restorative Sands", target, restorative_sands_heal, restorative_sands_crit)
        
        self.highest_stat = caster.find_highest_secondary_stat_rating()
        
        if self.highest_stat == "haste":
            caster.update_stat("haste", self.trinket_second_value)
        elif self.highest_stat == "crit":
            caster.update_stat("crit", self.trinket_second_value)
        elif self.highest_stat == "mastery":
            caster.update_stat("mastery", self.trinket_second_value)
        elif self.highest_stat == "versatility":
            caster.update_stat("versatility", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        if self.highest_stat == "haste":
            caster.update_stat("haste", -self.trinket_second_value)
        elif self.highest_stat == "crit":
            caster.update_stat("crit", -self.trinket_second_value)
        elif self.highest_stat == "mastery":
            caster.update_stat("mastery", -self.trinket_second_value)
        elif self.highest_stat == "versatility":
            caster.update_stat("versatility", -self.trinket_second_value)
        

class CoagulatedGenesaurBloodBuff(Buff):
    
    BASE_PPM = 1.66
    
    def __init__(self, caster):
        super().__init__("Coagulated Genesaur Blood", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # crit
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.update_stat("crit", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("crit", -self.trinket_first_value)
        

class SeaStarBuff(Buff):
    
    BASE_PPM = 1.5
    
    def __init__(self, caster):
        super().__init__("Sea Star", 15, base_duration=15)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):     
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        
        
class SustainingAlchemistStoneBuff(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Sustaining Alchemist Stone", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
        

class AlacritousAlchemistStoneBuff(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Alacritous Alchemist Stone", 10, base_duration=10)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # intellect
        self.trinket_first_value = trinket_values[0]
        
    def apply_effect(self, caster, current_time=None):        
        caster.spell_power += caster.get_effective_spell_power(self.trinket_first_value)
        caster.abilities["Potion"].remaining_cooldown -= 10
        caster.abilities["Potion"].shared_cooldown_end_time -= 10
        caster.abilities["Aerated Mana Potion"].remaining_cooldown -= 10
        caster.abilities["Elemental Potion of Ultimate Power"].remaining_cooldown -= 10
        
    def remove_effect(self, caster, current_time=None):
        caster.spell_power -= caster.get_effective_spell_power(self.trinket_first_value)
            
            
class PipsEmeraldFriendshipBadge(Buff):
    
    BASE_PPM = 2
    
    def __init__(self, caster):
        super().__init__("Pip's Emerald Friendship Badge", 10000, base_duration=10000)
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass
    

class BestFriendsWithPipEmpowered(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Pip Empowered", 12, base_duration=12)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.diminish_rate = 1/12
        self.diminished_value = 0
        self.last_update_time = 0
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", self.trinket_second_value)
        self.diminished_value = self.trinket_second_value
        self.last_update_time = current_time
        
    def remove_effect(self, caster, current_time, replaced=False):
        if not replaced:
            caster.apply_buff_to_self(BestFriendsWithPip(caster), current_time)
        caster.update_stat("mastery", -self.diminished_value)
            
    def diminish_effect(self, caster, current_time):
        time_since_update = current_time - self.last_update_time
        if time_since_update >= 1:
            self.diminished_value -= self.trinket_second_value * self.diminish_rate
            caster.update_stat("mastery", -self.trinket_second_value * self.diminish_rate)
            self.last_update_time = current_time
        
        
class BestFriendsWithPip(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Pip", 10000, base_duration=10000)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("mastery", -self.trinket_first_value)
        
        
class BestFriendsWithAerwynEmpowered(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Aerwyn Empowered", 12, base_duration=12)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.diminish_rate = 1/12
        self.diminished_value = 0
        self.last_update_time = 0
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.trinket_second_value)
        self.diminished_value = self.trinket_second_value
        self.last_update_time = current_time
        
    def remove_effect(self, caster, current_time, replaced=False):
        if not replaced:
            caster.apply_buff_to_self(BestFriendsWithAerwyn(caster), current_time)
        caster.update_stat("crit", -self.diminished_value)
            
    def diminish_effect(self, caster, current_time):
        time_since_update = current_time - self.last_update_time
        if time_since_update >= 1:
            self.diminished_value -= self.trinket_second_value * self.diminish_rate
            caster.update_stat("crit", -self.trinket_second_value * self.diminish_rate)
            self.last_update_time = current_time
        

class BestFriendsWithAerwyn(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Aerwyn", 10000, base_duration=10000)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("crit", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("crit", -self.trinket_first_value)
        
        
class BestFriendsWithUrctosEmpowered(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Urctos Empowered", 12, base_duration=12)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.diminish_rate = 1/12
        self.diminished_value = 0
        self.last_update_time = 0
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.trinket_second_value)
        self.diminished_value = self.trinket_second_value
        self.last_update_time = current_time
        
    def remove_effect(self, caster, current_time, replaced=False):
        if not replaced:
            caster.apply_buff_to_self(BestFriendsWithUrctos(caster), current_time)
        caster.update_stat("versatility", -self.diminished_value)
            
    def diminish_effect(self, caster, current_time):
        time_since_update = current_time - self.last_update_time
        if time_since_update >= 1:
            self.diminished_value -= self.trinket_second_value * self.diminish_rate
            caster.update_stat("versatility", -self.trinket_second_value * self.diminish_rate)
            self.last_update_time = current_time
        
        
class BestFriendsWithUrctos(Buff):
    
    def __init__(self, caster):
        super().__init__("Best Friends with Urctos", 10000, base_duration=10000)
        trinket_effect = caster.trinkets["Pip's Emerald Friendship Badge"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.trinket_first_value)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("versatility", -self.trinket_first_value)
        
        
        
class IdolOfTheSpellWeaverStacks(Buff):
    
    BASE_PPM = 2.2
    
    def __init__(self, caster):
        super().__init__("Idol of the Spell-Weaver", 10000, base_duration=10000, current_stacks=2, max_stacks=18)
        trinket_effect = caster.trinkets["Idol of the Spell-Weaver"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        self.malygite_count = caster.gem_counts["Malygite"]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("versatility", self.trinket_first_value * self.malygite_count)
        if caster.active_auras[self.name].current_stacks == 18:
            del caster.active_auras[self.name]
            self.remove_effect(caster, current_time)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("versatility", -self.trinket_first_value * 18)
        caster.apply_buff_to_self(IdolOfTheSpellWeaverEmpower(caster), current_time)
    

class IdolOfTheSpellWeaverEmpower(Buff):
    
    def __init__(self, caster):
        super().__init__("Idol of the Spell-Weaver Empowered", 15, base_duration=15)
        trinket_effect = caster.trinkets["Idol of the Spell-Weaver"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        self.malygite_count = caster.gem_counts["Malygite"]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.trinket_second_value / 4)
        caster.update_stat("crit", self.trinket_second_value / 4)
        caster.update_stat("mastery", self.trinket_second_value / 4)
        caster.update_stat("versatility", self.trinket_second_value / 4)
        
    def remove_effect(self, caster, current_time):
        caster.update_stat("haste", -self.trinket_second_value / 4)
        caster.update_stat("crit", -self.trinket_second_value / 4)
        caster.update_stat("mastery", -self.trinket_second_value / 4)
        caster.update_stat("versatility", -self.trinket_second_value / 4)
        

class EchoingTyrstoneBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Echoing Tyrstone", 15, base_duration=15)
        trinket_effect = caster.trinkets[self.name]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("haste", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("haste", -self.trinket_second_value)
        
        
class SmolderingSeedlingActive(Buff):
    
    def __init__(self, caster):
        super().__init__("Smoldering Seedling active", 12, base_duration=12)
        from .target import SmolderingSeedling
        
        trinket_effect = caster.trinkets["Smoldering Seedling"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
        self.smoldering_seedling = SmolderingSeedling("smoldering_seedling", caster)
        
    def apply_effect(self, caster, current_time=None):
        if self.smoldering_seedling not in caster.potential_healing_targets:
            caster.potential_healing_targets.append(self.smoldering_seedling)
        
    def remove_effect(self, caster, current_time=None):
        if self.smoldering_seedling in caster.potential_healing_targets:
            caster.potential_healing_targets.remove(self.smoldering_seedling)
        caster.apply_buff_to_self(SmolderingSeedlingBuff(caster), current_time)
        

class SmolderingSeedlingBuff(Buff):
    
    def __init__(self, caster):
        super().__init__("Smoldering Seedling", 10, base_duration=10)      
        trinket_effect = caster.trinkets["Smoldering Seedling"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        self.trinket_first_value = trinket_values[0]
        self.trinket_second_value = trinket_values[1]
        
    def apply_effect(self, caster, current_time=None):
        caster.update_stat("mastery", self.trinket_second_value)
        
    def remove_effect(self, caster, current_time=None):
        caster.update_stat("mastery", -self.trinket_second_value)
        

class BlossomOfAmirdrassilLargeHoT(HoT):
    
    def __init__(self, caster):
        super().__init__("Blossom of Amirdrassil Large HoT", 6, base_duration=6, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        self.time_until_next_tick = self.base_tick_interval
        trinket_effect = caster.trinkets["Blossom of Amirdrassil"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # initial hot
        self.trinket_first_value = trinket_values[0]
        
    def calculate_tick_healing(self, caster):
        total_healing = self.trinket_first_value * caster.versatility_multiplier
        
        if "Blessing of Spring" in caster.active_auras:
            total_healing *= 1.15
        
        number_of_ticks = self.base_duration / self.base_tick_interval
        healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        crit_chance = caster.crit
        random_num = random.random() * 100
        if random_num <= crit_chance:
            is_crit = True

        return healing_per_tick, is_crit


class BlossomOfAmirdrassilSmallHoT(HoT):
    
    def __init__(self, caster):
        super().__init__("Blossom of Amirdrassil Small HoT", 6, base_duration=6, base_tick_interval=1, initial_haste_multiplier=caster.haste_multiplier, hasted=False)
        self.time_until_next_tick = self.base_tick_interval
        trinket_effect = caster.trinkets["Blossom of Amirdrassil"]["effect"]
        trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
        
        # three target hot
        self.trinket_second_value = trinket_values[1]
        
    def calculate_tick_healing(self, caster):
        total_healing = self.trinket_second_value * caster.versatility_multiplier
        
        if "Blessing of Spring" in caster.active_auras:
            total_healing *= 1.15
        
        number_of_ticks = self.base_duration / self.base_tick_interval
        healing_per_tick = total_healing / number_of_ticks
        
        is_crit = False
        crit_chance = caster.crit
        random_num = random.random() * 100
        if random_num <= crit_chance:
            is_crit = True

        return healing_per_tick, is_crit
    

# embellishments
class PotionAbsorptionInhibitor(Buff):
    
    def __init__(self, caster):
        super().__init__("Potion Absorption Inhibitor", 10000, base_duration=10000)   
        if caster.embellishments["Potion Absorption Inhibitor"]["count"] == 2:
            self.current_stacks = 2
            self.max_stacks = 2
        
    def apply_effect(self, caster, current_time=None):
        pass
        
    def remove_effect(self, caster, current_time=None):
        pass