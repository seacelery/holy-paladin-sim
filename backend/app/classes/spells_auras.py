import random

from .spells import Spell
from .auras_buffs import AvengingWrathBuff, BeaconOfLightBuff, DivineFavorBuff, BlessingOfFreedomBuff, TyrsDeliveranceSelfBuff, TyrsDeliveranceTargetBuff, BlessingOfSummer, BlessingOfAutumn, BlessingOfWinter, BlessingOfSpring, FirebloodBuff, GiftOfTheNaaruBuff, HandOfDivinityBuff, BarrierOfFaithBuff, AvengingCrusaderBuff, DawnlightAvailable, DivinePurpose
from ..utils.misc_functions import append_aura_applied_event, format_time, update_spell_data_casts, update_spell_data_initialise_spell


# APPLIES BUFFS   
class BarrierOfFaithSpell(Spell):
    
    SPELL_POWER_COEFFICIENT = 5
    BASE_COOLDOWN = 30
    MANA_COST = 0.024

    def __init__(self, caster):
        super().__init__("Barrier of Faith", cooldown=BarrierOfFaithSpell.BASE_COOLDOWN, mana_cost=BarrierOfFaithSpell.MANA_COST, is_heal=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal, exclude_mastery=True, ignore_spell_multiplier=True)
        if cast_success:
            target = targets[0]
            
            target.apply_buff_to_target(BarrierOfFaithBuff(caster), current_time, caster=caster)
            
            if caster.ptr and caster.is_talent_active("Dawnlight"):
                caster.apply_buff_to_self(DawnlightAvailable(caster), current_time, stacks_to_apply=2, max_stacks=2)
                
            if caster.ptr and caster.is_talent_active("Aurora"):
                caster.apply_buff_to_self(DivinePurpose(), current_time, reapply=True)
            
        return cast_success, spell_crit, heal_amount
    

class BeaconOfFaithSpell(Spell):
    
    BASE_COOLDOWN = 0
    MANA_COST = 0.005
    
    def __init__(self, caster):
        super().__init__("Beacon of Faith", cooldown=BeaconOfFaithSpell.BASE_COOLDOWN, mana_cost=BeaconOfFaithSpell.MANA_COST, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            target = targets[0]
            
            target.apply_buff_to_target(BeaconOfLightBuff(caster), current_time, caster=caster)
            
        return cast_success, spell_crit, heal_amount
    

class BeaconOfVirtueSpell(Spell):
    
    BASE_COOLDOWN = 15
    MANA_COST = 0.04

    def __init__(self, caster):
        super().__init__("Beacon of Virtue", cooldown=BeaconOfVirtueSpell.BASE_COOLDOWN, mana_cost=BeaconOfVirtueSpell.MANA_COST)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            if not caster.beacon_targets:
                chosen_target = targets[0]
                secondary_targets = random.sample([target for target in caster.potential_healing_targets if target != chosen_target], 4)
                
                caster.beacon_targets = [chosen_target] + secondary_targets
                
                for target in caster.beacon_targets:
                    target.apply_buff_to_target(BeaconOfLightBuff(caster), current_time, caster=caster)
                
        return cast_success, spell_crit, heal_amount
        

class TyrsDeliveranceSpell(Spell):
    
    BASE_COOLDOWN = 90
    BASE_CAST_TIME = 2
    MANA_COST = 0.024
    
    def __init__(self, caster):
        super().__init__("Tyr's Deliverance", cooldown=TyrsDeliveranceSpell.BASE_COOLDOWN, base_cast_time=TyrsDeliveranceSpell.BASE_CAST_TIME, mana_cost=TyrsDeliveranceSpell.MANA_COST)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(TyrsDeliveranceSelfBuff(), current_time)
            
            for _ in range(5):
                target = [random.choice(caster.potential_healing_targets)]
                TyrsDeliveranceHeal(caster).cast_healing_spell(caster, target, current_time, is_heal=True)
            
            
class TyrsDeliveranceHeal(Spell):
    
    SPELL_POWER_COEFFICIENT = 0.626875
    
    def __init__(self, caster):
        super().__init__("Tyr's Deliverance", is_heal=True, off_gcd=True)
        if caster.ptr:
            # TODO VERIFY
            self.SPELL_POWER_COEFFICIENT *= 0.85
            
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            target = targets[0]
            target.apply_buff_to_target(TyrsDeliveranceTargetBuff(), current_time, caster=caster)  
            
            append_aura_applied_event(caster.events, "Tyr's Deliverance", caster, target, current_time, target.target_active_buffs["Tyr's Deliverance (target)"][0].duration)   
        
        return cast_success, spell_crit, heal_amount   
    
    
class AvengingWrathSpell(Spell):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Avenging Wrath", cooldown=AvengingWrathSpell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(AvengingWrathBuff(caster), current_time)
            
            
class AvengingCrusaderSpell(Spell):
    
    BASE_COOLDOWN = 60
    MANA_COST = 0.036
    HOLY_POWER_COST = 3
    
    def __init__(self, caster):
        super().__init__("Avenging Crusader", cooldown=AvengingCrusaderSpell.BASE_COOLDOWN, mana_cost=AvengingCrusaderSpell.MANA_COST, holy_power_cost=AvengingCrusaderSpell.HOLY_POWER_COST, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.holy_power -= self.holy_power_cost
            caster.apply_buff_to_self(AvengingCrusaderBuff(caster), current_time)
   
            
class DivineFavorSpell(Spell):
    
    BASE_COOLDOWN = 30
    
    def __init__(self, caster):
        super().__init__("Divine Favor", cooldown=DivineFavorSpell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(DivineFavorBuff(), current_time)
        
        return cast_success, spell_crit, heal_amount
     

class HandOfDivinitySpell(Spell):
    
    BASE_COOLDOWN = 90
    BASE_CAST_TIME = 1.5
    
    def __init__(self, caster):
        super().__init__("Hand of Divinity", cooldown=HandOfDivinitySpell.BASE_COOLDOWN, base_cast_time=HandOfDivinitySpell.BASE_CAST_TIME)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success, spell_crit, heal_amount = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(HandOfDivinityBuff(), current_time)
        
        return cast_success, spell_crit, heal_amount   
    
             
class BlessingOfTheSeasons(Spell):
    
    MANA_COST = 0.01
    BASE_COOLDOWN = 45
    
    def __init__(self, caster):
        super().__init__("Blessing of Summer", mana_cost=BlessingOfTheSeasons.MANA_COST, cooldown=BlessingOfTheSeasons.BASE_COOLDOWN)
        self.initial_cast = True
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            if self.initial_cast:
                update_spell_data_initialise_spell(caster.ability_breakdown, "Blessing of the Seasons")
                self.initial_cast = False
            
            caster.events.append(f"{format_time(current_time)}: {self.name} cast on {caster.name}")
            if self.name == "Blessing of Summer":
                if caster.seasons[self.name]:
                    caster.apply_buff_to_self(BlessingOfSummer(), current_time)
                self.name = "Blessing of Autumn"
                
            elif self.name == "Blessing of Autumn":
                if caster.seasons[self.name]:
                    caster.apply_buff_to_self(BlessingOfAutumn(), current_time)
                self.name = "Blessing of Winter"
                
            elif self.name == "Blessing of Winter":
                if caster.seasons[self.name]:
                    caster.apply_buff_to_self(BlessingOfWinter(), current_time)
                self.name = "Blessing of Spring"
                
            elif self.name == "Blessing of Spring":
                if caster.seasons[self.name]:
                    caster.apply_buff_to_self(BlessingOfSpring(), current_time)
                self.name = "Blessing of Summer"
                self.initial_cast = True
            
                
class FirebloodSpell(Spell):
    
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Fireblood", cooldown=FirebloodSpell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(FirebloodBuff(), current_time)
            

class GiftOfTheNaaruSpell(Spell):
    
    BASE_COOLDOWN = 180
    
    def __init__(self, caster):
        super().__init__("Gift of the Naaru", cooldown=GiftOfTheNaaruSpell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            targets[0].apply_buff_to_target(GiftOfTheNaaruBuff(caster), current_time, caster=caster)