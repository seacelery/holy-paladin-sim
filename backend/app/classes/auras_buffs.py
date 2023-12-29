import random

from .auras import Buff
from ..utils.misc_functions import append_spell_heal_event, format_time


class HoT(Buff):
    
    def __init__(self, name, duration, base_duration, base_tick_interval, initial_haste_multiplier, current_stacks=1, max_stacks=1):
        super().__init__(name, duration, base_duration, current_stacks=current_stacks, max_stacks=max_stacks) 
        self.base_tick_interval = base_tick_interval 
        self.time_until_next_tick = base_tick_interval
        self.total_ticks = 0
        self.previous_haste_multiplier = initial_haste_multiplier
        self.previous_tick_time = 0
        
    def add_stack(self, new_buff_instance):
        self.buff_instances.append(new_buff_instance)
    
    def update_tick_interval(self, caster):
        pass
        
    def process_tick(self, caster, target, current_time, buff_instances, is_partial_tick=False):
        # heal_value, is_crit = self.calculate_tick_healing(caster)
        total_heal_value, is_crit = self.calculate_tick_healing(caster) 
        total_heal_value *= len(buff_instances)
        
        if is_crit:
            total_heal_value *= 2
        
        if is_partial_tick:
            total_heal_value *= (current_time - self.previous_tick_time) / (self.base_tick_interval / caster.haste_multiplier)
        target.receive_heal(total_heal_value)
        if is_crit:
            caster.events.append(f"{format_time(current_time)}: Holy Reverberation crit healed {target.name} for {round(total_heal_value)}")
        else:
            caster.events.append(f"{format_time(current_time)}: Holy Reverberation healed {target.name} for {round(total_heal_value)}")
        self.total_ticks += 1 if not is_partial_tick else self.time_until_next_tick / self.base_tick_interval
        
        
    def calculate_tick_healing(self, caster):
        # spell_power = caster.stats.ratings["intellect"]
        spell_power = 9340
        
        total_healing = spell_power * self.SPELL_POWER_COEFFICIENT * caster.healing_multiplier
        
        mastery_multiplier = 1 + (caster.mastery_multiplier - 1) * caster.mastery_effectiveness
        versatility_multiplier = caster.versatility_multiplier
        total_healing *= mastery_multiplier * versatility_multiplier

        number_of_ticks = self.base_duration / (self.base_tick_interval / caster.haste_multiplier)
        if number_of_ticks > 1:
            total_healing *= caster.haste_multiplier
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
        
    def apply_effect(self, caster):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.crit += 15
        caster.healing_multiplier *= 1.15
        caster.damage_multiplier *= 1.15
        
    def remove_effect(self, caster):
        if caster.is_talent_active("Avenging Wrath: Might"):
            caster.crit -= 15
        caster.healing_multiplier /= 1.15
        caster.damage_multiplier /= 1.15
        
        
class DivineFavorBuff(Buff):
    
    def __init__(self):
        super().__init__("Divine Favor", 10000)
        
    def apply_effect(self, caster):
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].spell_healing_modifier *= 1.6
            caster.abilities["Holy Light"].cast_time_modifier *= 0.7
            caster.abilities["Holy Light"].mana_cost_modifier *= 0.5
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].spell_healing_modifier *= 1.6
            caster.abilities["Flash of Light"].cast_time_modifier *= 0.7
            caster.abilities["Flash of Light"].mana_cost_modifier *= 0.5
            
    def remove_effect(self, caster):
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
        
    def apply_effect(self, caster):
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].mana_cost_modifier *= 0
        
    def remove_effect(self, caster):
        if "Flash of Light" in caster.abilities:
            caster.abilities["Flash of Light"].mana_cost_modifier = 1
            if "Divine Favor" in caster.active_auras:
                caster.abilities["Flash of Light"].mana_cost_modifier *= 0.7
        if "Holy Light" in caster.abilities:
            caster.abilities["Holy Light"].holy_power_gain = 1


class DivineResonance(Buff):
    
    def __init__(self):
        super().__init__("Divine Resonance", 15)
        self.last_holy_shock_time = 0
        
    def apply_effect(self, caster):
        self.last_holy_shock_time = 0
    
    def increment_divine_resonance(self, caster, current_time, tick_rate):
        self.last_holy_shock_time += tick_rate
        if self.last_holy_shock_time >= 4.99:
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
        super().__init__("Rising Sunlight", 30, current_stacks=3, max_stacks=3)
       
        
class FirstLight(Buff):
    
    # casting Daybreak increases haste by 25% for 6 seconds
    def __init__(self):
        super().__init__("First Light", 6)
        
    def apply_effect(self, caster):
        caster.haste_multiplier *= 1.25
        caster.update_hasted_cooldowns_with_haste_changes()
    
    def remove_effect(self, caster):
        caster.haste_multiplier /= 1.25
        caster.update_hasted_cooldowns_with_haste_changes()
        
        
class AwakeningStacks(Buff):
    
    def __init__(self):
        super().__init__("Awakening", 60, base_duration=60, current_stacks=1, max_stacks=12)
       
        
class AwakeningTrigger(Buff):
    
    def __init__(self):
        super().__init__("Awakening READY!!!!!!", 30)
        
        
class TyrsDeliveranceSelfBuff(Buff):
    
    def __init__(self):
        super().__init__("Tyr's Deliverance (self)", 20)
        self.last_tyr_tick_time = 0
        self.base_tick_interval = 1
        
    def apply_effect(self, caster):
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

        spell.spell_healing_modifier *= (hasted_tick_interval - (hasted_tick_interval - self.last_tyr_tick_time)) / hasted_tick_interval
        spell.cast_healing_spell(caster, target, current_time, is_heal=True)
        spell.spell_healing_modifier /= (hasted_tick_interval - (hasted_tick_interval - self.last_tyr_tick_time)) / hasted_tick_interval
        
        
class DivinePurpose(Buff):
    
    def __init__(self):
        super().__init__("Divine Purpose", 12)
        
        
class BlessingOfDawn(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Dawn", 20, base_duration=20, current_stacks=1, max_stacks=2)
        
        
class BlessingOfDusk(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Dusk", 10)
      
        
class SophicDevotion(Buff):
    
    BASE_PPM = 1
    
    def __init__(self):
        super().__init__("Sophic Devotion", 15)
        
    def apply_effect(self, caster):
        caster.spell_power += 932
        print(f"EFFECT ACTIVE, NEW INT: {caster.spell_power}")
        
    def remove_effect(self, caster):
        caster.spell_power -= 932
        print(f"EFFECT ENDING, NEW INT: {caster.spell_power}")
 
 
# target buffs   

             
class GlimmerOfLightBuff(Buff):
    
    def __init__(self):
        super().__init__("Glimmer of Light", 30, base_duration=30)
    
    
class BlessingOfFreedomBuff(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Freedom", 8)
        
        
class TyrsDeliveranceTargetBuff(Buff):
    
    def __init__(self):
        super().__init__("Tyr's Deliverance (target)", 12)
        
        
class BlessingOfSummer(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Summer", 30)
        
        
class BlessingOfAutumn(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Autumn", 30)
        
        
class BlessingOfWinter(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Winter", 30)
        self.last_holy_shock_time = 0
        
    def apply_effect(self, caster):
        self.last_winter_tick_time = 0
        self.mana_gained = 0
    
    def increment_blessing_of_winter(self, caster, current_time, tick_rate):       
        self.last_winter_tick_time += tick_rate
        if self.last_winter_tick_time >= 1.99:
            caster.mana += caster.base_mana * 0.01
            self.mana_gained += caster.base_mana * 0.01
            # caster.events.append(f"{current_time}: {caster.base_mana * 0.01} mana restored by winter new caster mana {caster.mana}")
            self.last_winter_tick_time = 0
            
        if caster.active_auras["Blessing of Winter"].duration < 0.01:
            caster.events.append(f"{format_time(current_time)}: {caster.name} gained {round(self.mana_gained)} mana from Blessing of Winter")
    
    # def remove_effect(self, caster):
    #     caster.events.append(f"Mana after winter: {caster.mana}, {self.mana_gained}")    
    
    
class BlessingOfSpring(Buff):
    
    def __init__(self):
        super().__init__("Blessing of Spring", 30)
        
    def apply_effect(self, caster):
        caster.healing_multiplier *= 1.15
        
    def remove_effect(self, caster):
        caster.healing_multiplier /= 1.15