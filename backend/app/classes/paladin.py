import pprint
import copy
import heapq
import os
import json
import random
import sys
from dotenv import load_dotenv

from ..utils.misc_functions import format_time, append_aura_applied_event, append_aura_removed_event, append_aura_stacks_decremented, update_self_buff_data, calculate_beacon_healing, update_spell_data_beacon_heals, append_spell_beacon_event
from ..utils.buff_class_map import buff_class_map
from ..utils.beacon_transfer_rates import beacon_transfer
from ..utils.stat_values import diminishing_returns_values, stat_conversions, calculate_stat_percent_with_dr, calculate_leech_percent_with_dr, update_stat_with_multiplicative_percentage
from .spells import Wait
from .spells_healing import HolyShock, WordOfGlory, LightOfDawn, FlashOfLight, HolyLight, DivineToll, Daybreak, LightsHammerSpell, LayOnHands, HolyPrism, LightOfTheMartyr, EternalFlame
from .spells_misc import ArcaneTorrent, AeratedManaPotion, Potion, ElementalPotionOfUltimatePowerPotion, AuraMastery
from .spells_damage import Judgment, CrusaderStrike, HammerOfWrath, Consecration
from .spells_auras import AvengingWrathSpell, AvengingCrusaderSpell, DivineFavorSpell, TyrsDeliveranceSpell, BlessingOfTheSeasons, FirebloodSpell, GiftOfTheNaaruSpell, HandOfDivinitySpell, BarrierOfFaithSpell, BeaconOfFaithSpell, BeaconOfVirtueSpell
from .auras_buffs import PipsEmeraldFriendshipBadge, BestFriendsWithPip, BestFriendsWithAerwyn, BestFriendsWithUrctos, MercifulAuras, SavedByTheLight, OminousChromaticEssence, BroodkeepersPromiseHoT, IncarnatesMarkOfFire, MorningStar
from .trinkets import MirrorOfFracturedTomorrows, SmolderingSeedling, NymuesUnravelingSpindle, ConjuredChillglobe, TimeBreachingTalon, SpoilsOfNeltharus, MiniatureSingingStone
from ..utils.talents.talent_dictionaries import test_active_class_talents, test_active_spec_talents
from ..utils.talents.base_talent_dictionaries import base_active_class_talents, base_active_spec_talents, base_active_class_talents_ptr, base_active_spec_talents_ptr, base_active_lightsmith_talents, base_herald_of_the_sun_talents
from ..utils.gems_and_enchants import convert_enchants_to_stats, return_enchants_stats, return_gem_stats
from .api_client import APIClient

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

pp = pprint.PrettyPrinter(width=200)

# TODO
# seal of the crusader

class Stats:
    
    def __init__(self, ratings, percentages):
        self.ratings = ratings
        self.percentages = percentages
   
        
class Talents:
    
    def __init__(self, class_talents, spec_talents, lightsmith_talents=None, herald_of_the_sun_talents=None):
        self.class_talents = class_talents
        self.spec_talents = spec_talents
        
        self.lightsmith_talents = lightsmith_talents
        self.herald_of_the_sun_talents = herald_of_the_sun_talents


class Paladin:
    
    def __init__(self, name, character_data=None, stats_data=None, talent_data=None, equipment_data=None, buffs=None, consumables=None, potential_healing_targets=None, test=False, version=None):
        self.ptr = False
        if version == "ptr":
            self.ptr = True
        
        self.character_data = character_data if character_data else None
        self.race = self.character_data["race"]["name"] if self.character_data else None
        self.name = name[0].upper() + name[1:]
        self.test = test
        
        self.talents = self.parse_talents(talent_data)
        self.class_talents = copy.deepcopy(self.talents.class_talents)
        self.spec_talents = copy.deepcopy(self.talents.spec_talents)
        
        if self.ptr:
            self.lightsmith_talents = copy.deepcopy(self.talents.lightsmith_talents)
            self.herald_of_the_sun_talents = copy.deepcopy(self.talents.herald_of_the_sun_talents)
        
        self.base_mana = 250000
        self.mana = self.base_mana
        self.max_mana = self.base_mana
        self.mana_regen_per_second = 2000
        self.innervate_active = False
        
        self.base_flat_haste = 0
        self.base_flat_crit = 5
        self.base_flat_mastery = 12
        self.base_flat_versatility = 0
        
        self.flat_haste = 0
        self.flat_crit = 5
        self.flat_mastery = 12
        self.flat_versatility = 0
        self.flat_leech = 0
        
        self.active_auras = {}
        self.gem_counts = {}
        self.total_elemental_gems = 0
        
        if equipment_data:
            self.equipment = self.parse_equipment(equipment_data)
            formatted_equipment_data = self.calculate_stats_from_equipment(self.equipment)
            self.stats = Stats(formatted_equipment_data[0], self.convert_stat_ratings_to_percent(formatted_equipment_data[0]))
            self.bonus_enchants = formatted_equipment_data[1]
            
            self.spell_power = self.stats.ratings["intellect"]          
            self.haste_rating = self.stats.ratings["haste"]
            self.crit_rating = self.stats.ratings["crit"]
            self.mastery_rating = self.stats.ratings["mastery"]
            self.versatility_rating = self.stats.ratings["versatility"]
            self.max_health = self.stats.ratings["stamina"] * 20
            self.leech_rating = self.stats.ratings["leech"]
            
            self.haste, self.crit, self.mastery, self.versatility, self.leech = self.convert_stat_ratings_to_percent(self.stats.ratings)
            
            # initialise base stats for use in race changes
            self.base_spell_power = self.get_effective_spell_power(self.spell_power)
            self.base_haste = self.haste
            self.base_crit = self.crit
            self.base_mastery = self.mastery
            self.base_versatility = self.versatility
            self.base_max_health = self.max_health
            
            self.base_haste_rating = self.haste_rating
            self.base_crit_rating = self.crit_rating
            self.base_mastery_rating = self.mastery_rating
            self.base_versatility_rating = self.versatility_rating
        else:
            self.spell_power, self.haste, self.crit, self.mastery, self.leech = 0
            self.bonus_enchants = []
        
        self.base_crit_damage_modifier = 1
        self.base_crit_healing_modifier = 1
        self.crit_damage_modifier = 1
        self.crit_healing_modifier = 1
        
        # initialise raid buffs & consumables
        self.buffs = buffs
        self.consumables = {}
        self.initial_consumables = {}
        
        self.trinkets = {}
        self.update_trinkets()
        
        self.embellishments = {}
        self.update_embellishments()
        
        self.set_bonuses = {"season_1": 0, "season_2": 0, "season_3": 0}
        
        # initialise abilities
        self.abilities = {}      
        self.load_abilities_based_on_talents()
        
        # initialise stats with racials
        self.update_stats_with_racials()
        
        self.base_global_cooldown = 1.5
        self.hasted_global_cooldown = self.base_global_cooldown / self.haste_multiplier
        self.global_cooldown = 0
        
        self.holy_power = 0
        self.max_holy_power = 5
        self.holy_power_gained = 0
        self.holy_power_wasted = 0
        
        self.self_healing = 0
        
        self.currently_casting = None
        self.remaining_cast_time = 0
        
        self.total_casts = {}
        self.healing_by_ability = {}
        self.cast_sequence = []
        self.healing_sequence = []
        self.ability_crits = {}
        self.events = []
        
        self.beacon_events = []
        self.buff_events = []
        self.ability_cast_events = []
        self.holy_power_by_ability = {}
        
        self.potential_healing_targets = potential_healing_targets
        self.glimmer_targets = {}
        self.beacon_targets = []
        self.glimmer_application_counter = 0
        self.glimmer_removal_counter = 0
        
        self.mastery_effectiveness = 0.95
        self.average_raid_health_percentage = 0.7
        self.variable_target_counts = {"Light of Dawn": 5, "Light's Hammer": 6, "Resplendent Light": 5}
        self.seasons = {"summer": True, "autumn": True, "winter": True, "spring": True}
        self.is_enemy_below_20_percent = False
        
        self.time_based_stacking_buffs = {}
        self.active_summons = {}
        self.time_since_last_rppm_proc = {}
        self.time_since_last_rppm_proc_attempt = {}
        self.conditional_effect_cooldowns = {}
        self.healing_multiplier = 1
        self.damage_multiplier = 1
        
        self.holy_shock_cooldown_overflow = 0
        self.infused_holy_light_count = 0
        self.divine_resonance_timer = 0
        self.divine_toll_holy_shock_count = 0
        self.delayed_casts = []
        self.rising_sunlight_timer = 0
        self.tyrs_deliverance_extended_by = 0
        self.blessing_of_dawn_counter = 0
        self.afterimage_counter = 0
        self.awakening_queued = False
        self.holy_shock_resets = 0
        self.external_buff_timers = {}
        self.timers_priority_queue = []
        self.extra_consecration_count = 0
              
        # for results output only
        self.last_iteration = False
        self.ability_breakdown = {}
        self.self_buff_breakdown = []
        self.target_buff_breakdown = []
        self.glimmer_counts = {0: 0}
        self.tyrs_counts = {0: 0}
        self.awakening_counts = {0: 0}
        self.awakening_trigger_times = {}
        self.healing_timeline = {}
        self.mana_timeline = {0: self.max_mana}
        self.holy_power_timeline = {0: 0}
        self.mana_breakdown = {}
        self.holy_power_breakdown = {}
        self.priority_breakdown = {} 
        
        self.total_glimmer_healing = 0
        self.glimmer_hits = 0
        
    def reset_state(self):
        current_state = copy.deepcopy(self.initial_state)
        self.__dict__.update(current_state.__dict__)
        
    # update properties methods used in routes.py
    def update_character(self, race=None, class_talents=None, spec_talents=None, lightsmith_talents=None, herald_of_the_sun_talents=None, consumables=None):
        if consumables:
            self.update_consumables(consumables)
        if race:
            self.update_race(race)
        if class_talents:
            self.update_class_talents(class_talents)
        if spec_talents:
            self.update_spec_talents(spec_talents)
        if lightsmith_talents:
            self.update_lightsmith_talents(lightsmith_talents)
        if herald_of_the_sun_talents:
            self.update_herald_of_the_sun_talents(herald_of_the_sun_talents)
        
        self.update_abilities()
        self.initial_state = copy.deepcopy(self)
        
    def update_consumables(self, new_consumables):
        if "flask" in new_consumables:
            self.consumables["flask"] = new_consumables["flask"]
            self.initial_consumables["flask"] = new_consumables["flask"]
        if "augment_rune" in new_consumables:
            self.consumables["augment_rune"] = new_consumables["augment_rune"]
            self.initial_consumables["augment_rune"] = new_consumables["augment_rune"]
        if "food" in new_consumables:
            self.consumables["food"] = new_consumables["food"]
            self.initial_consumables["food"] = new_consumables["food"]
        if "weapon_imbue" in new_consumables:
            self.consumables["weapon_imbue"] = new_consumables["weapon_imbue"]
            self.initial_consumables["weapon_imbue"] = new_consumables["weapon_imbue"]
        if "raid_buff" in new_consumables:
            self.consumables["raid_buff"] = new_consumables["raid_buff"]
            self.initial_consumables["raid_buff"] = new_consumables["raid_buff"]
        if "external_buff" in new_consumables:
            self.consumables["external_buff"] = new_consumables["external_buff"]
            self.initial_consumables["external_buff"] = new_consumables["external_buff"]
    
    def update_race(self, new_race):
        self.race = new_race
    
    def update_class_talents(self, talents):
        for talent_name, new_rank in talents.items():
            for row in self.class_talents.values():
                if talent_name in row:
                    row[talent_name]["ranks"]["current rank"] = new_rank 
        
    def update_spec_talents(self, talents):
        for talent_name, new_rank in talents.items(): 
            for row in self.spec_talents.values():
                if talent_name in row:
                    row[talent_name]["ranks"]["current rank"] = new_rank 
                    
    def update_lightsmith_talents(self, talents):
        for talent_name, new_rank in talents.items(): 
            for row in self.lightsmith_talents.values():
                if talent_name in row:
                    row[talent_name]["ranks"]["current rank"] = new_rank 
                    
    def update_herald_of_the_sun_talents(self, talents):
        for talent_name, new_rank in talents.items(): 
            for row in self.herald_of_the_sun_talents.values():
                if talent_name in row:
                    row[talent_name]["ranks"]["current rank"] = new_rank 
                    
    def update_equipment(self, equipment_data):  
        if self.test:      
            self.equipment = json.loads(equipment_data)
        else:
            self.equipment = equipment_data
        
        formatted_equipment_data = self.calculate_stats_from_equipment(self.equipment)
        self.stats = Stats(formatted_equipment_data[0], self.convert_stat_ratings_to_percent(formatted_equipment_data[0]))
        self.bonus_enchants = formatted_equipment_data[1]
        
        self.spell_power = self.stats.ratings["intellect"]       
        self.haste_rating = self.stats.ratings["haste"]
        self.crit_rating = self.stats.ratings["crit"]
        self.mastery_rating = self.stats.ratings["mastery"]
        self.versatility_rating = self.stats.ratings["versatility"]
        self.max_health = self.stats.ratings["stamina"] * 20
        self.leech_rating = self.stats.ratings["leech"]
        
        self.haste, self.crit, self.mastery, self.versatility, self.leech = self.convert_stat_ratings_to_percent(self.stats.ratings)
        
        # initialise base stats for use in race changes
        self.base_spell_power = self.get_effective_spell_power(self.spell_power)
        self.base_haste = self.haste
        self.base_crit = self.crit
        self.base_mastery = self.mastery
        self.base_versatility = self.versatility
        self.base_max_health = self.max_health
        
        self.base_haste_rating = self.haste_rating
        self.base_crit_rating = self.crit_rating
        self.base_mastery_rating = self.mastery_rating
        self.base_versatility_rating = self.versatility_rating
        
        self.update_stats_with_racials()
        self.hasted_global_cooldown = self.base_global_cooldown / self.haste_multiplier
        self.update_abilities()
        self.update_trinkets()
        self.update_embellishments()
    
    def update_trinkets(self):
        self.trinkets = {}
        
        for item in self.equipment:
            if item in ["trinket_1", "trinket_2"]:
                trinket_data = self.equipment[item]
                self.trinkets[trinket_data["name"]] = {"item_level": trinket_data["item_level"], "effect": trinket_data["effects"][0]["description"], "option": trinket_data["effects"][0].get("trinket_options", None)}
                
    def update_embellishments(self):
        self.embellishments = {}
        
        for item in self.equipment:
            
            if self.equipment[item]["limit"] == "Unique-Equipped: Embellished (2)":
                embellishment_data = self.equipment[item]["effects"][0]
                name = embellishment_data["name"]
                self.embellishments[name] = {
                                             "effect": embellishment_data["description"], 
                                             "count": self.embellishments.get(name, {"count": 0})["count"] + 1
                                            }
    
    # update loadout based on updated properties 
    def apply_consumables(self):
        consumable_buffs = []
        
        for consumable_type, consumable_list in self.consumables.items():
            if consumable_list:                
                for consumable_name in consumable_list:
                    if consumable_type == "external_buff":
                        external_buff_timers = consumable_list[consumable_name]
                        self.external_buff_timers[consumable_name] = external_buff_timers
                    
                    if consumable_type != "external_buff":
                        consumable_class = buff_class_map.get(consumable_name)
                        if consumable_class:
                            consumable_buffs.append(consumable_class)   
                            
                for buff, timers in self.external_buff_timers.items():
                    for timer in timers:
                        if timer != "":
                            heapq.heappush(self.timers_priority_queue, (float(timer), buff))                
        
        for buff in consumable_buffs:
            self.apply_buff_to_self(buff(), 0)
        
        # reinitialise potions    
        self.abilities["Potion"] = Potion(self)
        self.abilities["Aerated Mana Potion"] = AeratedManaPotion(self)
        self.abilities["Elemental Potion of Ultimate Power"] = ElementalPotionOfUltimatePowerPotion(self)
        
    def apply_item_effects(self):
        item_effect_buffs = {}
        
        for effect_name, effect_data in self.embellishments.items():
            effect =  effect_data["effect"]
            effect_count = effect_data["count"]
            
            item_effect_buffs[buff_class_map.get(effect_name)] = effect_count
        
        for buff, buff_count in item_effect_buffs.items():
            buff_instance = buff(self)
            if buff_instance.base_duration == 10000:
                self.apply_buff_to_self(buff_instance, 0, buff_count, 2)    
                           
    def update_abilities(self):
        self.load_abilities_based_on_talents()
        self.update_abilities_with_racials()
        self.update_stats_with_racials()
        
    def update_stat(self, stat, stat_rating):
        if stat == "haste":
            if self.race == "Human":
                self.haste_rating += stat_rating * 1.02
            else:
                self.haste_rating += stat_rating
            self.haste = calculate_stat_percent_with_dr(self, "haste", self.haste_rating, self.flat_haste)
            self.haste_multiplier = (self.haste / 100) + 1
        if stat == "crit":
            if self.race == "Human":
                self.crit_rating += stat_rating * 1.02
            else:
                self.crit_rating += stat_rating
            self.crit = calculate_stat_percent_with_dr(self, "crit", self.crit_rating, self.flat_crit)
            self.crit_multiplier = (self.crit / 100) + 1
        if stat == "mastery":
            if self.race == "Human":
                self.mastery_rating += stat_rating * 1.02
            else:
                self.mastery_rating += stat_rating
            self.mastery = calculate_stat_percent_with_dr(self, "mastery", self.mastery_rating, self.flat_mastery)
            self.mastery_multiplier = (self.mastery / 100) + 1
        if stat == "versatility":
            if self.race == "Human":
                self.versatility_rating += stat_rating * 1.02
            else:
                self.versatility_rating += stat_rating
            self.versatility = calculate_stat_percent_with_dr(self, "versatility", self.versatility_rating, self.flat_versatility)
            self.versatility_multiplier = (self.versatility / 100) + 1
        if stat == "leech":
            self.leech_rating += stat_rating
            self.leech = calculate_leech_percent_with_dr(self, "leech", self.leech_rating, self.flat_leech)
            
        if stat == "haste" and "Time Warp" in self.active_auras:
            update_stat_with_multiplicative_percentage(self, "haste", 30, True)
        if stat == "haste" and "First Light" in self.active_auras:
            update_stat_with_multiplicative_percentage(self, "haste", 25, True)
            
    def update_stats_with_racials(self):   
        # reset stats
        self.spell_power = self.base_spell_power
        self.haste = self.base_haste
        self.crit = self.base_crit
        self.mastery = self.base_mastery
        self.versatility = self.base_versatility
        self.max_health = self.base_max_health
        
        self.haste_rating = self.base_haste_rating
        self.crit_rating = self.base_crit_rating
        self.mastery_rating = self.base_mastery_rating
        self.versatility_rating = self.base_versatility_rating
        
        self.crit_damage_modifier = self.base_crit_damage_modifier
        self.crit_healing_modifier = self.base_crit_healing_modifier
        
        # update stats based on race
        if self.race == "Human":
            # self.haste = (self.base_haste - 4) * 1.02 + 4
            # self.crit = (self.base_crit - 9) * 1.02 + 9
            # self.mastery = (self.base_mastery - 6 - 12) * 1.02 + 6 + 12
            # self.versatility = self.base_versatility * 1.02
            
            self.haste_rating = self.base_haste_rating * 1.02
            self.crit_rating = self.base_crit_rating * 1.02
            self.mastery_rating = self.base_mastery_rating * 1.02
            self.versatility_rating = self.base_versatility_rating * 1.02
            
            self.haste, self.crit, self.mastery, self.versatility, self.leech = self.convert_stat_ratings_to_percent({"haste": self.haste_rating, "crit": self.crit_rating, 
                                                                                                                      "mastery": self.mastery_rating, "versatility": self.versatility_rating, 
                                                                                                                      "leech": self.leech_rating})
        elif self.race == "Dwarf":
            self.crit_damage_modifier = self.base_crit_damage_modifier + 0.02
            self.crit_healing_modifier = self.base_crit_healing_modifier + 0.02
        elif self.race == "Draenei":
            self.spell_power = self.base_spell_power + (113 * 1.05 * 1.04)
        elif self.race == "Lightforged Draenei":
            pass
        elif self.race == "Dark Iron Dwarf":
            pass
        elif self.race == "Blood Elf":
            self.flat_crit = self.base_flat_crit + 1
            self.update_stat("crit", 0)
        elif self.race == "Tauren":
            self.crit_damage_modifier = self.base_crit_damage_modifier + 0.02
            self.crit_healing_modifier = self.base_crit_healing_modifier + 0.02
            self.max_health += 197 * 20
        elif self.race == "Zandalari Troll":
            pass
        
        self.update_stat_multipliers()
        
    def update_stat_multipliers(self):
        self.haste_multiplier = (self.haste / 100) + 1
        self.crit_multiplier = (self.crit / 100) + 1
        self.mastery_multiplier = (self.mastery / 100) + 1
        self.versatility_multiplier = (self.versatility / 100) + 1 
    
    def update_abilities_with_racials(self):
        if self.race == "Blood Elf":
            self.abilities["Arcane Torrent"] = ArcaneTorrent(self) 
        elif self.race == "Dark Iron Dwarf":
            self.abilities["Fireblood"] = FirebloodSpell(self)
        elif self.race == "Draenei":
            self.abilities["Gift of the Naaru"] = GiftOfTheNaaruSpell(self)
        
    def load_abilities_based_on_talents(self):
        self.abilities = {
                            "Wait": Wait(),
                            "Flash of Light": FlashOfLight(self),
                            "Holy Light": HolyLight(self),
                            "Crusader Strike": CrusaderStrike(self),
                            "Judgment": Judgment(self),
                            "Consecration": Consecration(self),
                            "Lay on Hands": LayOnHands(self),
                            "Aerated Mana Potion": AeratedManaPotion(self),
                            "Elemental Potion of Ultimate Power": ElementalPotionOfUltimatePowerPotion(self),
                            "Potion": Potion(self)
        }     
        
        if self.ptr and self.is_talent_active("Eternal Flame"):
            self.abilities["Eternal Flame"] = EternalFlame(self)
        else:
            self.abilities["Word of Glory"] = WordOfGlory(self)
        
        if self.is_talent_active("Holy Shock"):
            self.abilities["Holy Shock"] = HolyShock(self)
            
        if self.is_talent_active("Divine Toll") and self.is_talent_active("Holy Shock"):
            self.abilities["Divine Toll"] = DivineToll(self)
            
        if self.is_talent_active("Daybreak") and self.is_talent_active("Glimmer of Light") and self.is_talent_active("Holy Shock"):
            self.abilities["Daybreak"] = Daybreak(self)
            
        if self.is_talent_active("Light of Dawn"):
            self.abilities["Light of Dawn"] = LightOfDawn(self)
            
        if self.is_talent_active("Avenging Wrath"):
            if self.is_talent_active("Avenging Crusader"):
                self.abilities["Avenging Crusader"] = AvengingCrusaderSpell(self)
            else:
                self.abilities["Avenging Wrath"] = AvengingWrathSpell(self)
            
        if self.is_talent_active("Hammer of Wrath"):
            self.abilities["Hammer of Wrath"] = HammerOfWrath(self)
            
        if self.is_talent_active("Divine Favor"):
            self.abilities["Divine Favor"] = DivineFavorSpell(self)
            
        if self.is_talent_active("Hand of Divinity"):
            self.abilities["Hand of Divinity"] = HandOfDivinitySpell(self)
         
        if self.is_talent_active("Aura Mastery"):
            self.abilities["Aura Mastery"] = AuraMastery(self) 
            
        if self.is_talent_active("Barrier of Faith"):
            self.abilities["Barrier of Faith"] = BarrierOfFaithSpell(self)
         
        if self.is_talent_active("Beacon of Faith"):
            self.abilities["Beacon of Faith"] = BeaconOfFaithSpell(self) 
            
        if self.is_talent_active("Beacon of Virtue"):
            self.abilities["Beacon of Virtue"] = BeaconOfVirtueSpell(self)
            
        if self.is_talent_active("Tyr's Deliverance") and self.is_talent_active("Holy Shock"):
            self.abilities["Tyr's Deliverance"] = TyrsDeliveranceSpell(self)
            
        if self.is_talent_active("Holy Prism"):
            self.abilities["Holy Prism"] = HolyPrism(self)
            
        if self.is_talent_active("Blessing of Summer"):
            self.abilities["Blessing of the Seasons"] = BlessingOfTheSeasons(self)
            
        if not self.ptr:
            if self.is_talent_active("Light's Hammer"):
                self.abilities["Light's Hammer"] = LightsHammerSpell(self)
            
            if self.is_talent_active("Light of the Martyr"):
                self.abilities["Light of the Martyr"] = LightOfTheMartyr(self)
            
        # trinkets
        if self.is_trinket_equipped("Miniature Singing Stone"):
            self.abilities["Miniature Singing Stone"] = MiniatureSingingStone(self)
        
        if self.is_trinket_equipped("Mirror of Fractured Tomorrows"):
            self.abilities["Mirror of Fractured Tomorrows"] = MirrorOfFracturedTomorrows(self)
            
        if self.is_trinket_equipped("Smoldering Seedling"):
            self.abilities["Smoldering Seedling"] = SmolderingSeedling(self)
            
        if self.is_trinket_equipped("Nymue's Unraveling Spindle"):
            self.abilities["Nymue's Unraveling Spindle"] = NymuesUnravelingSpindle(self)
            
        if self.is_trinket_equipped("Conjured Chillglobe"):
            self.abilities["Conjured Chillglobe"] = ConjuredChillglobe(self)
            
        if self.is_trinket_equipped("Time-Breaching Talon"):
            self.abilities["Time-Breaching Talon"] = TimeBreachingTalon(self)
            
        if self.is_trinket_equipped("Spoils of Neltharus"):
            self.abilities["Spoils of Neltharus"] = SpoilsOfNeltharus(self)
            
        # ptr abilities
        if self.ptr:
            pass
        
        # ptr trinkets
        if self.ptr:
            pass
            
    def is_talent_active(self, talent_name):
        for row, talents in self.class_talents.items():
            if talent_name in talents and talents[talent_name]["ranks"]["current rank"] > 0:
                return True, talents[talent_name]["ranks"]["current rank"]
        
        for row, talents in self.spec_talents.items():
            if talent_name in talents and talents[talent_name]["ranks"]["current rank"] > 0:
                return True, talents[talent_name]["ranks"]["current rank"]
            
        if self.ptr:    
            for row, talents in self.lightsmith_talents.items():
                if talent_name in talents and talents[talent_name]["ranks"]["current rank"] > 0:
                    return True, talents[talent_name]["ranks"]["current rank"]
                
            for row, talents in self.herald_of_the_sun_talents.items():
                if talent_name in talents and talents[talent_name]["ranks"]["current rank"] > 0:
                    return True, talents[talent_name]["ranks"]["current rank"]

        return False
    
    def is_trinket_equipped(self, trinket_name):
        if trinket_name in self.equipment["trinket_1"]["name"] or trinket_name in self.equipment["trinket_2"]["name"]:
            return True
        
        return False
    
    def apply_buffs_on_encounter_start(self):
        if self.is_trinket_equipped("Pip's Emerald Friendship Badge"):
            self.apply_buff_to_self(PipsEmeraldFriendshipBadge(self), 0)
            self.apply_buff_to_self(random.choice([BestFriendsWithPip(self), BestFriendsWithAerwyn(self), BestFriendsWithUrctos(self)]), 0)
            
        if self.is_trinket_equipped("Ominous Chromatic Essence"):
            self.apply_buff_to_self(OminousChromaticEssence(self), 0)
            
        if self.is_trinket_equipped("Whispering Incarnate Icon"):
            self.apply_buff_to_self(IncarnatesMarkOfFire(self), 0)
            
        if self.is_trinket_equipped("Broodkeeper's Promise"):
            targets = random.sample(self.potential_healing_targets, 2)
            
            for target in targets:
                target.apply_buff_to_target(BroodkeepersPromiseHoT(self), 0, caster=self)
            
        if self.is_talent_active("Merciful Auras"):
            self.apply_buff_to_self(MercifulAuras(), 0)
            
        if self.is_talent_active("Saved by the Light"):
            self.apply_buff_to_self(SavedByTheLight(), 0)
            
        if self.ptr and self.is_talent_active("Morning Star"):
            self.apply_buff_to_self(MorningStar(self), 0)
    
    # misc simulation functions 
    def print_stats(self, current_time):
        print(f"{round(current_time, 2)}: sp {self.spell_power}, haste {round(self.base_haste, 2)}, crit {round(self.base_crit, 2)}, mast {round(self.base_mastery, 2)}, vers {round(self.base_versatility, 2)}, crit heal {round(self.crit_healing_modifier, 2)}")
    
    def update_hasted_cooldowns_with_haste_changes(self):
        for ability in self.abilities.values():
            if ability.hasted_cooldown and ability.original_cooldown is not None:
                elapsed_cooldown = ability.original_cooldown - ability.remaining_cooldown
                ability.remaining_cooldown = ability.calculate_cooldown(self) - elapsed_cooldown * (ability.calculate_cooldown(self) / ability.original_cooldown)
                
    def find_highest_secondary_stat_rating(self):
        stats = {
            "haste": self.haste_rating,
            "crit": self.crit_rating,
            "mastery": self.mastery_rating,
            "versatility": self.versatility_rating
        }
        
        return max(stats, key=stats.get)
                
    def check_cooldowns(self):
        spell_cooldowns = {}
        
        for ability_name, ability in self.abilities.items():
            if ability.current_charges == ability.max_charges:
                ability.remaining_cooldown = 0
            spell_cooldowns[ability_name] = {"remaining_cooldown": ability.remaining_cooldown, "base_cooldown": ability.original_cooldown, 
                                             "current_charges": ability.current_charges, "max_charges": ability.max_charges}
            
        return spell_cooldowns
    
    def check_external_buff_timers(self, current_time):
        while self.timers_priority_queue and current_time >= self.timers_priority_queue[0][0]:
            timer, buff = heapq.heappop(self.timers_priority_queue)
            buff_class = buff_class_map.get(buff)
            self.apply_buff_to_self(buff_class(), timer)
            
    def check_stats(self):
        stats = {
            "haste": {},
            "crit": {},
            "mastery": {},
            "versatility": {},
            "intellect": {}
        }
        
        stats["haste"]["haste_rating"] = self.haste_rating
        stats["haste"]["base_haste_rating"] = self.base_haste_rating
        stats["haste"]["haste"] = self.haste
        stats["haste"]["base_haste"] = self.base_haste
        stats["haste"]["haste_multiplier"] = self.haste_multiplier
        
        stats["crit"]["crit_rating"] = self.crit_rating
        stats["crit"]["base_crit_rating"] = self.base_crit_rating
        stats["crit"]["crit"] = self.crit
        stats["crit"]["base_crit"] = self.base_crit
        stats["crit"]["crit_multiplier"] = self.crit_multiplier
        
        stats["mastery"]["mastery_rating"] = self.mastery_rating
        stats["mastery"]["base_mastery_rating"] = self.base_mastery_rating
        stats["mastery"]["mastery"] = self.mastery
        stats["mastery"]["base_mastery"] = self.base_mastery
        stats["mastery"]["mastery_multiplier"] = self.mastery_multiplier
        
        stats["versatility"]["versatility_rating"] = self.versatility_rating
        stats["versatility"]["base_versatility_rating"] = self.base_versatility_rating
        stats["versatility"]["versatility"] = self.versatility
        stats["versatility"]["base_versatility"] = self.base_versatility
        stats["versatility"]["versatility_multiplier"] = self.versatility_multiplier
        
        stats["intellect"]["intellect"] = self.spell_power
        
        return stats
    
    def get_effective_spell_power(self, spell_power):
        # 5% from plate armour bonus
        spell_power *= 1.05
        
        # seal of might bonus
        if self.is_talent_active("Seal of Might") and self.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 1:
            return spell_power * 1.02
        elif self.is_talent_active("Seal of Might") and self.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 2:
            return spell_power * 1.04
        return spell_power
            
    def receive_self_heal(self, amount):
        self.self_healing += amount
        
    def handle_beacon_healing(self, spell_name, target, initial_heal, current_time, spell_display_name=None):      
        if spell_name not in beacon_transfer:
            return
        
        if spell_name == "Light of the Martyr" and "Maraad's Dying Breath" not in self.active_auras:
            return
        
        beacon_healing = calculate_beacon_healing(spell_name, initial_heal, self)
        
        for beacon_target in self.beacon_targets:
            if target != beacon_target:
                beacon_target.receive_beacon_heal(beacon_healing)
                self.healing_by_ability["Beacon of Light"] = self.healing_by_ability.get("Beacon of Light", 0) + beacon_healing    
                
                update_spell_data_beacon_heals(self.ability_breakdown, beacon_target, beacon_healing, spell_display_name if spell_display_name else spell_name)
                
                append_spell_beacon_event(self.beacon_events, spell_display_name if spell_display_name else spell_name, self, beacon_target, initial_heal, beacon_healing, current_time)   
        
    def update_gcd(self, tick_rate):     
        self.hasted_global_cooldown = self.base_global_cooldown / self.haste_multiplier
           
        if self.global_cooldown > 0:
            self.global_cooldown = max(0, self.global_cooldown - tick_rate)
            
    def set_beacon_targets(self):
        beacon_targets = []
        
        if self.is_talent_active("Beacon of Faith"):
            beacon_targets = random.sample(self.potential_healing_targets, 2)
        elif not self.is_talent_active("Beacon of Virtue"):
            beacon_targets = random.sample(self.potential_healing_targets, 1)
        
        self.beacon_targets = beacon_targets
    
    # handle auras and summons on self
    def apply_summon(self, summon, current_time):
        self.active_summons[summon.name] = summon
        self.events.append(f"{format_time(current_time)}: {summon.name} created: {summon.duration}s")
        summon.apply_effect(self, current_time)
   
    def apply_buff_to_self(self, buff, current_time, stacks_to_apply=1, max_stacks=1, reapply=False, apply_effect_at_max_stacks=True): 
        if buff.name in self.active_auras and not reapply:
            append_aura_applied_event(self.events, f"{self.active_auras[buff.name].name} reapplied", self, self, current_time, self.active_auras[buff.name].duration)
            if not apply_effect_at_max_stacks and buff.current_stacks == max_stacks:
                pass
            else:
                buff.apply_effect(self, current_time)
               
            if buff.current_stacks < max_stacks:
                buff.current_stacks += stacks_to_apply
                buff.duration = buff.base_duration
                self.active_auras[buff.name] = buff
        else:
            self.active_auras[buff.name] = buff
            buff.apply_effect(self, current_time)
            append_aura_applied_event(self.events, self.active_auras[buff.name].name, self, self, current_time, self.active_auras[buff.name].duration)
        
        buff.times_applied += 1
        update_self_buff_data(self.self_buff_breakdown, buff.name, current_time, "applied", buff.duration, buff.current_stacks)

    def extend_buff_on_self(self, buff, current_time, time_extension):
        if buff.name in self.active_auras:
            self.active_auras[buff.name].duration += time_extension
            self.events.append(f"{format_time(current_time)}: {buff.name} extended by {time_extension}s to {round(self.active_auras[buff.name].duration, 2)}s")
            
        update_self_buff_data(self.self_buff_breakdown, buff.name, current_time, "extended", buff.duration, buff.current_stacks, time_extension)
    
    def remove_or_decrement_buff_on_self(self, buff, current_time, max_stacks=1, replaced=False):
        if buff.name in self.active_auras:
            if buff.current_stacks > 1:
                buff.current_stacks -= 1
                append_aura_stacks_decremented(self.events, buff.name, self, current_time, buff.current_stacks, duration=self.active_auras[buff.name].duration)
                
                update_self_buff_data(self.self_buff_breakdown, buff.name, current_time, "stacks_decremented", buff.duration, buff.current_stacks)
            else:
                del self.active_auras[buff.name]
                if replaced:
                    buff.remove_effect(self, current_time, replaced)
                else:
                    buff.remove_effect(self, current_time)
                
                update_self_buff_data(self.self_buff_breakdown, buff.name, current_time, "expired")
                
    def choose_multiple_targets(self, ability, non_beacon_targets):
        targets = []
                    
        beacon_targets = self.beacon_targets.copy()
        
        if beacon_targets:
            # 3 means beacon targets chosen 15% of the time for some reason i don't really know
            num_beacon_targets = random.choices([0, 1], weights=[1, 3], k=1)[0]
            
            for _ in range(num_beacon_targets):
                beacon_target = random.choice(beacon_targets)
                targets.append(beacon_target)
                beacon_targets.remove(beacon_target)
            
        remaining_targets_count = ability.healing_target_count - len(targets)
        
        num_targets_to_add = min(len(non_beacon_targets), remaining_targets_count)
        if num_targets_to_add > 0:
            targets.extend(random.sample(non_beacon_targets, min(len(non_beacon_targets), remaining_targets_count)))
        return targets
    
    # functions for parsing gear and loadout    
    def parse_stats(self, stats_data):
        ratings = {
            "health": stats_data["health"],
            "mana": stats_data["power"],
            "intellect": stats_data["intellect"]["effective"],
            "haste": stats_data["spell_haste"]["rating"],
            "crit": stats_data["spell_crit"]["rating"],
            "mastery": stats_data["mastery"]["rating"],
            "versatility": stats_data["versatility"],
            "leech": stats_data["lifesteal"]["rating"],
            "stamina": stats_data["stamina"]["effective"]
        }
        # (percent from rating, total percent)
        percentages = {
            "haste": (stats_data["spell_haste"]["rating_bonus"], stats_data["spell_haste"]["value"]),
            "crit": (stats_data["spell_crit"]["rating_bonus"], stats_data["spell_crit"]["value"]),
            "mastery": (stats_data["mastery"]["rating_bonus"], stats_data["mastery"]["value"]),
            "versatility": (stats_data["versatility_healing_done_bonus"], stats_data["versatility_healing_done_bonus"]),
            "leech": (stats_data["lifesteal"]["rating_bonus"], stats_data["lifesteal"]["value"])
        }
          
        return Stats(ratings, percentages)
    
    def parse_equipment(self, equipment_data):
        equipment = {}
        
        equipped_items = equipment_data["equipped_items"]
        
        for item in equipped_items:
            item_slot = item["slot"]["type"].lower()
            
            # exclude these slots
            if item_slot in ["shirt", "tabard"]:
                continue
            
            item_id = item['item']['id']
            item_name = item["name"]["en_GB"]
            item_level = item["level"]["value"]
            limit = item.get("limit_category", {}).get("en_GB")
            item_quality = item.get("quality").get("name").get("en_GB")
            effects = []
            media_reference_url = item["media"]["key"]["href"]
            api_client = APIClient()
            item_icon = api_client.get_item_media(media_reference_url)["assets"][0]["value"]
            
            stats_dict = {}
            
            equipment[item_slot] = { "name": item_name, "item_level": item_level, "stats": stats_dict, "item_id": item_id, "item_icon": item_icon, "quality": item_quality, "limit": limit, "effects": effects }
            
            if "stats" in item:
                for stat in item["stats"]:
                    stat_type = stat["type"]["type"].lower()
                    # filter irrelevant stats
                    if stat_type not in ["strength", "agility"]:
                        stat_value = stat["value"]
                        stats_dict[stat_type] = stat_value
                        
            enchantments = item.get("enchantments", [])
            item_enchantments = [enchantment["display_string"]["en_GB"] for enchantment in enchantments]
            if item_enchantments:
                equipment[item_slot]["enchantments"] = item_enchantments

            sockets = item.get("sockets", [])
            item_gems = [socket["item"]["name"]["en_GB"] for socket in sockets if socket.get("item")]
            if item_gems:
                equipment[item_slot]["gems"] = item_gems
                
            for effect in item.get("spells", []):
                effect_data = {
                    "name": effect.get("spell", {}).get("name", {}).get("en_GB", "Unknown effect name"),
                    "id": effect.get("spell", {}).get("id", "No ID"),
                    "description": effect.get("description", {}).get("en_GB", "No description")
                }
                equipment[item_slot]["effects"].append(effect_data)

        # rename stats
        rename_dict = {
            "combat_rating_lifesteal": "leech",
            "crit_rating": "crit",
            "haste_rating": "haste",
            "mastery_rating": "mastery"
        }
        
        for item_slot, item_data in equipment.items():
            stats = item_data.get("stats", {})
            for old_key, new_key in rename_dict.items():
                if old_key in stats:
                    stats[new_key] = stats.pop(old_key)
                
        return equipment
  
    def calculate_stats_from_equipment(self, equipment):
        stat_values_from_equipment = {}
        enchants_from_equipment = []
        gems_from_equipment = []
        bonus_effect_enchants = []
        
        self.set_bonuses = {"season_1": 0, "season_2": 0, "season_3": 0}
        
        for item_slot, item_data in equipment.items():
            
            name = item_data.get("name", "")
            if "Virtuous Silver" in name:
                self.set_bonuses["season_1"] += 1
            if "Heartfire Sentinel" in name:
                self.set_bonuses["season_2"] += 1
            if "Zealous Pyreknight" in name:
                self.set_bonuses["season_3"] += 1
            
            stats = item_data.get("stats", {})
            if stats:
                for stat in stats:
                    stat_values_from_equipment[stat] = stat_values_from_equipment.get(stat, 0) + stats[stat]
            
            enchants = item_data.get("enchantments", {})
            if enchants:
                for enchant in enchants:
                    enchants_from_equipment.append(enchant)
            
            gems = item_data.get("gems", {})
            if gems:
                for gem in gems:
                    gems_from_equipment.append(gem)
                
        formatted_enchants = convert_enchants_to_stats(enchants_from_equipment)
        
        return_enchants_stats(self, formatted_enchants, bonus_effect_enchants, stat_values_from_equipment)
        return_gem_stats(self, gems_from_equipment, stat_values_from_equipment)
         
        stat_values_from_equipment["intellect"] += 2089
        
        stat_values_from_equipment["stamina"] += 3848
        if self.is_talent_active("Sanctified Plates") and self.class_talents["row6"]["Sanctified Plates"]["ranks"]["current rank"] == 1:
            stat_values_from_equipment["stamina"] *= 1.03
        elif self.is_talent_active("Sanctified Plates") and self.class_talents["row6"]["Sanctified Plates"]["ranks"]["current rank"] == 2:
            stat_values_from_equipment["stamina"] *= 1.06
        
        return stat_values_from_equipment, bonus_effect_enchants
    
    def convert_stat_ratings_to_percent(self, stat_values):
        haste_rating = stat_values["haste"]
        crit_rating = stat_values["crit"]
        mastery_rating = stat_values["mastery"]
        versatility_rating = stat_values["versatility"]
        leech_rating = stat_values["leech"] if "leech" in stat_values else 0
        
        # 2% haste per point from seal of alacrity, multiplicative
        haste_percent = calculate_stat_percent_with_dr(self, "haste", haste_rating, self.flat_haste)
            
        # 5% bonus crit
        crit_percent = calculate_stat_percent_with_dr(self, "crit", crit_rating, self.flat_crit)
            
        # 12% base mastery
        mastery_percent = calculate_stat_percent_with_dr(self, "mastery", mastery_rating, self.flat_mastery)
            
        versatility_percent = calculate_stat_percent_with_dr(self, "versatility", versatility_rating, self.flat_versatility)
        
        leech_percent = calculate_leech_percent_with_dr(self, "leech", leech_rating, self.flat_leech)
        
        return haste_percent, crit_percent, mastery_percent, versatility_percent, leech_percent
    
    def parse_talents(self, talent_data):
        class_talents = {}
        spec_talents = {}
        
        if self.ptr:
            lightsmith_talents = {}
            herald_of_the_sun_talents = {}

        if self.ptr:
            active_class_talents = copy.deepcopy(base_active_class_talents_ptr)
            active_spec_talents = copy.deepcopy(base_active_spec_talents_ptr)
            
            active_lightsmith_talents = copy.deepcopy(base_active_lightsmith_talents)
            active_herald_of_the_sun_talents = copy.deepcopy(base_herald_of_the_sun_talents)
        else:
            active_class_talents = copy.deepcopy(base_active_class_talents)
            active_spec_talents = copy.deepcopy(base_active_spec_talents)

        class_talent_data = talent_data["specializations"][0]["loadouts"][0]["selected_class_talents"]
        for talent in class_talent_data:
            talent_name = talent["tooltip"]["talent"]["name"]
            talent_rank = talent["rank"]
            class_talents[talent_name] = talent_rank
            
        spec_talent_data = talent_data["specializations"][0]["loadouts"][0]["selected_spec_talents"]
        for talent in spec_talent_data:
            talent_name = talent["tooltip"]["talent"]["name"]
            talent_rank = talent["rank"]
            spec_talents[talent_name] = talent_rank    
        
        for talent_row, talents in active_class_talents.items():
            for talent_name, talent_info in talents.items():
                if talent_name in class_talents:
                    active_class_talents[talent_row][talent_name]["ranks"]["current rank"] = class_talents[talent_name]
                    
        for talent_row, talents in active_spec_talents.items():
            for talent_name, talent_info in talents.items():
                if talent_name in spec_talents:
                    active_spec_talents[talent_row][talent_name]["ranks"]["current rank"] = spec_talents[talent_name]
                    
        if self.ptr:
            # lightsmith_talent_data = talent_data["specializations"][0]["loadouts"][0]["selected_lightsmith_talents"]
            # for talent in lightsmith_talent_data:
            #     talent_name = talent["tooltip"]["talent"]["name"]
            #     talent_rank = talent["rank"]
            #     lightsmith_talents[talent_name] = talent_rank
                
            # herald_of_the_sun_talent_data = talent_data["specializations"][0]["loadouts"][0]["selected_herald_of_the_sun_talents"]
            # for talent in herald_of_the_sun_talent_data:
            #     talent_name = talent["tooltip"]["talent"]["name"]
            #     talent_rank = talent["rank"]
            #     herald_of_the_sun_talents[talent_name] = talent_rank  
                
            for talent_row, talents in active_lightsmith_talents.items():
                for talent_name, talent_info in talents.items():
                    if talent_name in class_talents:
                        active_lightsmith_talents[talent_row][talent_name]["ranks"]["current rank"] = lightsmith_talents[talent_name]
                        
            for talent_row, talents in active_herald_of_the_sun_talents.items():
                for talent_name, talent_info in talents.items():
                    if talent_name in spec_talents:
                        active_herald_of_the_sun_talents[talent_row][talent_name]["ranks"]["current rank"] = herald_of_the_sun_talents[talent_name]
        
        if self.ptr:
            return Talents(active_class_talents, active_spec_talents, active_lightsmith_talents, active_herald_of_the_sun_talents)
        else:           
            return Talents(active_class_talents, active_spec_talents)