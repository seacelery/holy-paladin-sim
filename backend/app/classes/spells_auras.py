import random

from .spells import Spell
from .auras_buffs import AvengingWrathBuff, DivineFavorBuff, BlessingOfFreedomBuff, TyrsDeliveranceSelfBuff, TyrsDeliveranceTargetBuff, BlessingOfSummer, BlessingOfAutumn, BlessingOfWinter, BlessingOfSpring
from ..utils.misc_functions import append_aura_applied_event, format_time, update_spell_data_casts, update_spell_data_initialise_spell

# APPLIES BUFFS   

     
class TyrsDeliveranceSpell(Spell):
    
    SPELL_ID = 200652
    BASE_COOLDOWN = 120
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
    
    SPELL_ID = 200652
    SPELL_POWER_COEFFICIENT = 0.626875
    
    def __init__(self, caster):
        super().__init__("Tyr's Deliverance", is_heal=True, off_gcd=True)
            
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            target = targets[0]
            target.apply_buff_to_target(TyrsDeliveranceTargetBuff(), current_time, caster=caster)  
            
            append_aura_applied_event(caster.events, "Tyr's Deliverance", caster, target, current_time, target.target_active_buffs["Tyr's Deliverance (target)"][0].duration)      
    
    
class AvengingWrathSpell(Spell):
    
    SPELL_ID = 31884
    BASE_COOLDOWN = 120
    
    def __init__(self, caster):
        super().__init__("Avenging Wrath", cooldown=AvengingWrathSpell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(AvengingWrathBuff(), current_time)
   
            
class DivineFavorSpell(Spell):
    
    SPELL_ID = 210294
    BASE_COOLDOWN = 30
    
    def __init__(self, caster):
        super().__init__("Divine Favor", cooldown=DivineFavorSpell.BASE_COOLDOWN, off_gcd=True)
        
    def cast_healing_spell(self, caster, targets, current_time, is_heal):
        cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
        if cast_success:
            caster.apply_buff_to_self(DivineFavorBuff(), current_time)
            
            
# class BlessingOfFreedomSpell(Spell):
    
#     MANA_COST = 0.014
#     BASE_COOLDOWN = 25
    
#     def __init__(self, caster):
#         super().__init__("Blessing of Freedom", mana_cost=BlessingOfFreedomSpell.MANA_COST, cooldown=BlessingOfFreedomSpell.BASE_COOLDOWN, applies_buff_to_target=True)
        
#     def cast_healing_spell(self, caster, targets, current_time, is_heal):
#         cast_success = super().cast_healing_spell(caster, targets, current_time, is_heal)
#         if cast_success:
#             chosen_target = random.choice(targets)
#             chosen_target.apply_buff_to_target(BlessingOfFreedomBuff(), current_time)
#             append_aura_applied_event(caster.buff_events, self.name, caster, chosen_target, current_time)
            
            
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
                caster.apply_buff_to_self(BlessingOfSummer(), current_time)
                self.name = "Blessing of Autumn"
                
            elif self.name == "Blessing of Autumn":
                caster.apply_buff_to_self(BlessingOfAutumn(), current_time)
                self.name = "Blessing of Winter"
                
            elif self.name == "Blessing of Winter":
                caster.apply_buff_to_self(BlessingOfWinter(), current_time)
                self.name = "Blessing of Spring"
                
            elif self.name == "Blessing of Spring":
                caster.apply_buff_to_self(BlessingOfSpring(), current_time)
                self.name = "Blessing of Summer"
                self.initial_cast = True
                
# class BlessingOfSummer(Spell):
#     SPELL_ID = 388007
    
#     def __init__(self, caster):
#         super().__init__("Blessing of Summer", mana_cost=BlessingOfTheSeasons.MANA_COST, cooldown=BlessingOfTheSeasons.BASE_COOLDOWN)

# class BlessingOfAutumn(Spell):
#     SPELL_ID = 388010
    
#     def __init__(self, caster):
#         super().__init__("Blessing of Summer", mana_cost=BlessingOfTheSeasons.MANA_COST, cooldown=BlessingOfTheSeasons.BASE_COOLDOWN)
    
# class BlessingOfWinter(Spell):
#     SPELL_ID = 388015
    
#     def __init__(self, caster):
#         super().__init__("Blessing of Summer", mana_cost=BlessingOfTheSeasons.MANA_COST, cooldown=BlessingOfTheSeasons.BASE_COOLDOWN)
    
# class BlessingOfSpring(Spell):
#     SPELL_ID = 388013
    
#     def __init__(self, caster):
#         super().__init__("Blessing of Summer", mana_cost=BlessingOfTheSeasons.MANA_COST, cooldown=BlessingOfTheSeasons.BASE_COOLDOWN)