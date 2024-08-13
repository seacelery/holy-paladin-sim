import re
import random

from .spells import Spell
from .auras_buffs import MirrorOfFracturedTomorrowsBuff, SmolderingSeedlingActive, NymuesUnravelingSpindleBuff, OvinaxsMercurialEggPaused, EtherealPowerlink, ImperfectAscendancySerumBuff, SpymastersWebBuff
from ..utils.misc_functions import update_mana_gained, update_spell_data_heals, update_spell_data_casts, add_talent_healing_multipliers


class Trinket(Spell):
    
    def __init__(self, name, cooldown=0, off_gcd=True, base_cast_time=0, hasted_cast_time=False):
        super().__init__(name, cooldown=cooldown, off_gcd=off_gcd, base_cast_time=base_cast_time, hasted_cast_time=hasted_cast_time)
  
  
class MiniatureSingingStone(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Miniature Singing Stone", cooldown=MiniatureSingingStone.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            update_spell_data_casts(caster.ability_breakdown, self.name, 0, 0, 0)
            
            trinket_effect = caster.trinkets[self.name]["effect"]
            trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
            
            # absorb
            self.trinket_first_value = trinket_values[0]
            
            target_count = 5
            
            targets = random.sample(caster.potential_healing_targets, target_count)
            for target in targets:            
                miniature_singing_stone_absorb = self.trinket_first_value * caster.versatility_multiplier

                target.receive_heal(miniature_singing_stone_absorb, caster)
                update_spell_data_heals(caster.ability_breakdown, "Miniature Singing Stone", target, miniature_singing_stone_absorb, False)
                
                caster.handle_beacon_healing("Miniature Singing Stone", target, miniature_singing_stone_absorb, current_time)
    
    
class MirrorOfFracturedTomorrows(Trinket):
    
    BASE_COOLDOWN = 180
    
    def __init__(self, caster):
        super().__init__("Mirror of Fractured Tomorrows", cooldown=MirrorOfFracturedTomorrows.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(MirrorOfFracturedTomorrowsBuff(caster), current_time)
            

class EchoingTyrstone(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Echoing Tyrstone Cast", cooldown=EchoingTyrstone.BASE_COOLDOWN, off_gcd=True)
        self.tyrstone_start_time = 0
        self.tyrstone_end_time = 0
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            self.tyrstone_start_time = current_time
            self.tyrstone_end_time = current_time + 10
            

class SmolderingSeedling(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Smoldering Seedling", cooldown=SmolderingSeedling.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(SmolderingSeedlingActive(caster), current_time)
            
            
class NymuesUnravelingSpindle(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Nymue's Unraveling Spindle", cooldown=NymuesUnravelingSpindle.BASE_COOLDOWN, base_cast_time=3, hasted_cast_time=False, off_gcd=False)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(NymuesUnravelingSpindleBuff(caster), current_time)
            

class ConjuredChillglobe(Trinket):
    
    BASE_COOLDOWN = 60
    
    def __init__(self, caster):
        super().__init__("Conjured Chillglobe", cooldown=ConjuredChillglobe.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            trinket_effect = caster.trinkets[self.name]["effect"]
            trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
            
            # damage
            self.trinket_first_value = trinket_values[0]
            # mana gain
            self.trinket_second_value = trinket_values[1]
            
            if caster.mana > caster.max_mana * 0.65:
                pass
            else:
                caster.mana += self.trinket_second_value
                update_mana_gained(caster.ability_breakdown, self.name, self.trinket_second_value)
                

class TimeBreachingTalon(Trinket):
    
    BASE_COOLDOWN = 150
    
    def __init__(self, caster):
        super().__init__("Time-Breaching Talon", cooldown=TimeBreachingTalon.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            from .auras_buffs import TimeBreachingTalonPlus
            
            caster.apply_buff_to_self(TimeBreachingTalonPlus(caster), current_time)
            

class SpoilsOfNeltharus(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Spoils of Neltharus", cooldown=SpoilsOfNeltharus.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            from .auras_buffs import SpoilsOfNeltharusBuff
            
            caster.apply_buff_to_self(SpoilsOfNeltharusBuff(caster), current_time)
            
            
class HighSpeakersAccretion(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("High Speaker's Accretion", cooldown=HighSpeakersAccretion.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            from .auras_buffs import HighSpeakersAccretionRift
            
            caster.apply_buff_to_self(HighSpeakersAccretionRift(caster), current_time)
            

class SiphoningPhylacteryShard(Trinket):
    
    BASE_COOLDOWN = 30
    
    def __init__(self, caster):
        super().__init__("Siphoning Phylactery Shard", cooldown=SiphoningPhylacteryShard.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            update_spell_data_casts(caster.ability_breakdown, self.name, 0, 0, 0)
            
            trinket_effect = caster.trinkets[self.name]["effect"]
            trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
            
            # self-damage
            self.trinket_first_value = trinket_values[0]
            # heal
            self.trinket_second_value = trinket_values[1]
       
            siphoning_phylactery_shard_heal = (self.trinket_second_value - self.trinket_first_value) * caster.versatility_multiplier
            siphoning_phylactery_shard_heal = add_talent_healing_multipliers(siphoning_phylactery_shard_heal, caster)

            targets[0].receive_heal(siphoning_phylactery_shard_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Siphoning Phylactery Shard", targets[0], siphoning_phylactery_shard_heal, False)
            
            caster.handle_beacon_healing("Siphoning Phylactery Shard", targets[0], siphoning_phylactery_shard_heal, current_time)
            

class CreepingCoagulum(Trinket):
    
    SPELL_POWER_COEFFICIENT = 0
    BASE_COOLDOWN = 90
    
    def __init__(self, caster):
        super().__init__("Creeping Coagulum", cooldown=CreepingCoagulum.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            update_spell_data_casts(caster.ability_breakdown, self.name, 0, 0, 0)
            
            trinket_effect = caster.trinkets[self.name]["effect"]
            trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
            
            # healing redirected
            self.trinket_first_value = trinket_values[0]
            creeping_coagulum_negative_heal = -self.trinket_first_value
            targets[0].receive_heal(creeping_coagulum_negative_heal, caster)
            update_spell_data_heals(caster.ability_breakdown, "Creeping Coagulum ", targets[0], creeping_coagulum_negative_heal, False)
            
            # heal
            self.trinket_second_value = trinket_values[1]     
            chosen_targets = random.sample(caster.potential_healing_targets, 5)
            for target in chosen_targets:
                creeping_coagulum_heal, creeping_coagulum_crit = CreepingCoagulum(caster).calculate_heal(caster)
                creeping_coagulum_heal = self.trinket_second_value * caster.versatility_multiplier   
                
                if creeping_coagulum_crit:
                    creeping_coagulum_heal *= 2 * caster.crit_healing_modifier * caster.crit_multiplier
                    
                creeping_coagulum_heal = add_talent_healing_multipliers(creeping_coagulum_heal, caster)
                    
                target.receive_heal(creeping_coagulum_heal, caster)
                update_spell_data_heals(caster.ability_breakdown, "Creeping Coagulum", target, creeping_coagulum_heal, creeping_coagulum_crit)
                

class OvinaxsMercurialEgg(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Ovinax's Mercurial Egg", cooldown=OvinaxsMercurialEgg.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(OvinaxsMercurialEggPaused(caster), current_time)
            

class TreacherousTransmitter(Trinket):
    
    BASE_COOLDOWN = 90
    
    def __init__(self, caster):
        super().__init__("Treacherous Transmitter", cooldown=TreacherousTransmitter.BASE_COOLDOWN, off_gcd=True)
    
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:          
            caster.apply_buff_to_self(EtherealPowerlink(caster), current_time)
        
        
class ImperfectAscendancySerumSpell(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Imperfect Ascendancy Serum", cooldown=ImperfectAscendancySerumSpell.BASE_COOLDOWN, base_cast_time=1.5, hasted_cast_time=False, off_gcd=False)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:          
            caster.apply_buff_to_self(ImperfectAscendancySerumBuff(caster), current_time)
            

class SpymastersWebSpell(Trinket):
    
    BASE_COOLDOWN = 20
    
    def __init__(self, caster):
        super().__init__("Spymaster's Web", cooldown=SpymastersWebSpell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:          
            caster.apply_buff_to_self(SpymastersWebBuff(caster), current_time)
            

class CorruptedEggShell(Trinket):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Corrupted Egg Shell", cooldown=CorruptedEggShell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:          
            update_spell_data_casts(caster.ability_breakdown, self.name, 0, 0, 0)
            
            trinket_effect = caster.trinkets[self.name]["effect"]
            trinket_values = [int(value.replace(",", "")) for value in re.findall(r"\*(\d+,?\d+)", trinket_effect)]
            
            # absorb
            self.trinket_first_value = trinket_values[0]
            
            target_count = 1
            targets = random.sample(caster.potential_healing_targets, target_count)
            
            for target in targets:            
                corrupted_egg_shell_absorb = self.trinket_first_value * caster.versatility_multiplier

                target.receive_heal(corrupted_egg_shell_absorb, caster)
                update_spell_data_heals(caster.ability_breakdown, self.name, target, corrupted_egg_shell_absorb, False)
                
                caster.handle_beacon_healing(self.name, target, corrupted_egg_shell_absorb, current_time)
            
            corrupted_egg_shell_mana_gain = caster.max_mana * 0.05
            caster.mana += corrupted_egg_shell_mana_gain
            update_mana_gained(caster.ability_breakdown, self.name, corrupted_egg_shell_mana_gain)
                
            