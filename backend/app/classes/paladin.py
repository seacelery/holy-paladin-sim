import pprint
import copy

from ..utils.misc_functions import format_time, append_aura_applied_event, append_aura_removed_event, append_aura_stacks_decremented, update_self_buff_data, calculate_beacon_healing, update_spell_data_beacon_heals, append_spell_beacon_event
from ..utils.beacon_transfer_rates import beacon_transfer_rates_single_beacon, beacon_transfer_rates_double_beacon
from .auras_buffs import PhialOfTepidVersatility, PhialOfElementalChaos
from .spells import Wait
from .spells_healing import HolyShock, WordOfGlory, LightOfDawn, FlashOfLight, HolyLight, DivineToll, Daybreak, LightsHammerSpell
from .spells_misc import ArcaneTorrent, AeratedManaPotion, Potion, ElementalPotionOfUltimatePowerPotion
from .spells_damage import Judgment, CrusaderStrike
from .spells_auras import AvengingWrathSpell, DivineFavorSpell, TyrsDeliveranceSpell, BlessingOfTheSeasons, FirebloodSpell, GiftOfTheNaaruSpell
from ..utils.talents.talent_dictionaries import test_active_class_talents, test_active_spec_talents
from ..utils.talents.base_talent_dictionaries import base_active_class_talents, base_active_spec_talents
from ..utils.gems_and_enchants import convert_enchants_to_stats, return_enchants_stats, return_gem_stats

pp = pprint.PrettyPrinter(width=200)


class Stats:
    
    def __init__(self, ratings, percentages):
        self.ratings = ratings
        self.percentages = percentages
   
        
class Talents:
    
    def __init__(self, class_talents, spec_talents):
        self.class_talents = class_talents
        self.spec_talents = spec_talents


class Paladin:
    
    def __init__(self, name, character_data=None, stats_data=None, talent_data=None, equipment_data=None, buffs=None, consumables=None, potential_healing_targets=None):
        self.character_data = character_data if character_data else None
        self.race = self.character_data["race"]["name"] if self.character_data else None
        self.name = name[0].upper() + name[1:]
        # self.stats = self.parse_stats(stats_data)
        # self.class_talents = self.parse_talents(talent_data)[0]
        # self.spec_talents = self.parse_talents(talent_data)[1]
        
        # self.talents = self.parse_talents(talent_data)
        # self.class_talents = copy.deepcopy(self.talents.class_talents)
        # self.spec_talents = copy.deepcopy(self.talents.spec_talents)
        
        # self.class_talents = self.parse_talents(talent_data)
        # self.spec_talents = self.parse_talents(talent_data)
        
        # self.talents = self.parse_talents(talent_data)
        self.class_talents = copy.deepcopy(test_active_class_talents)
        self.spec_talents = copy.deepcopy(test_active_spec_talents)
        
        # self.class_talents = copy.deepcopy(base_active_class_talents)
        # self.spec_talents = copy.deepcopy(base_active_spec_talents)
        
        # self.class_talents["row10"]["Divine Resonance"]["ranks"]["current rank"] = 1
        
        # self.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] = 0
        # print(self.class_talents["row3"]["Greater Judgment"])
        
        self.base_mana = 250000
        self.mana = self.base_mana
        self.max_mana = self.base_mana
        self.mana_regen_per_second = 2000
        
        if equipment_data:
            self.equipment = self.parse_equipment(equipment_data)
            formatted_equipment_data = self.calculate_stats_from_equipment(self.equipment)
            print(formatted_equipment_data)
            self.stats = Stats(formatted_equipment_data[0], self.convert_stat_ratings_to_percent(formatted_equipment_data[0]))
            self.bonus_enchants = formatted_equipment_data[1]
            print(self.stats.ratings)
            
            self.spell_power = self.stats.ratings["intellect"]
            print(self.spell_power)
            
            self.haste_rating = self.stats.ratings["haste"]
            self.crit_rating = self.stats.ratings["crit"]
            self.mastery_rating = self.stats.ratings["mastery"]
            self.versatility_rating = self.stats.ratings["versatility"]
            self.max_health = self.stats.ratings["stamina"] * 20
            self.leech = self.stats.ratings["leech"]
            # print(self.haste_rating, self.crit_rating, self.mastery_rating, self.versatility_rating)
            
            self.haste, self.crit, self.mastery, self.versatility = self.convert_stat_ratings_to_percent(self.stats.ratings)
            # print(self.haste, self.crit, self.mastery, self.versatility)
            
            # initialise base stats for use in race changes
            self.base_spell_power = self.get_effective_spell_power(self.spell_power)
            self.base_haste = self.haste
            self.base_crit = self.crit
            self.base_mastery = self.mastery
            self.base_versatility = self.versatility
            self.base_max_health = self.max_health
        else:
            self.spell_power = 9340
            self.haste = 22.98
            self.crit = 19.12
            # self.crit = 100
            self.mastery = 24.79
            self.versatility = 21.49
            self.stats = Stats({}, None)
            self.stats.ratings["health"] = 450000
            self.bonus_enchants = []
        
        print(f"Haste: {self.haste}, Crit: {self.crit}, Mastery: {self.mastery}, Vers: {self.versatility}")
        
        # self.haste_multiplier = (self.haste / 100) + 1
        # self.crit_multiplier = (self.crit / 100) + 1
        # self.mastery_multiplier = (self.mastery / 100) + 1
        # self.versatility_multiplier = (self.versatility / 100) + 1
        # print(self.haste_multiplier, self.crit_multiplier, self.mastery_multiplier, self.versatility_multiplier)
        
        # initialise raid buffs & consumables
        self.buffs = buffs
        self.consumables = {}
        
        # initialise abilities
        self.abilities = {}      
        self.load_abilities_based_on_talents()
        
        # initialise stats with racials
        self.update_stats_with_racials()
        self.crit_damage_modifier = 1
        self.crit_healing_modifier = 1
        
        self.mastery_effectiveness = 1
        print(self.max_health)
        
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
        
        self.active_auras = {}
        self.active_summons = {}
        self.time_since_last_rppm_proc = {}
        self.time_since_last_rppm_proc_attempt = {}
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
        
        # for reclamation
        self.average_raid_health_percentage = 0.7
        
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
        
        # self.apply_consumables()
        
        self.initial_state = copy.deepcopy(self)
    
    def reset_state(self):
        current_state = copy.deepcopy(self.initial_state)
        self.__dict__.update(current_state.__dict__)
        
    # update properties methods used in routes.py
    def update_character(self, race=None, class_talents=None, spec_talents=None, consumables=None):
        if consumables:
            self.update_consumables(consumables)
        if race:
            self.update_race(race)
        if class_talents:
            self.update_class_talents(class_talents)
        if spec_talents:
            self.update_spec_talents(spec_talents)
        
        self.update_abilities()
        
    def update_consumables(self, new_consumables):
        if new_consumables["flask"]:
            self.consumables["flask"] = new_consumables["flask"]
        self.apply_consumables()
    
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
    
    # update loadout based on updated properties 
    def apply_consumables(self):
        flask_name_split = self.consumables["flask"].split()
        for i, word in enumerate(flask_name_split):
            if word.lower() == "of":
                flask_name_split[i] = word.capitalize()
        flask_name = "".join(flask_name_split)
        
        flask_class = globals().get(flask_name)
        self.apply_buff_to_self(flask_class(), 0)
                   
    def update_abilities(self):
        self.load_abilities_based_on_talents()
        self.update_abilities_with_racials()
        self.update_stats_with_racials()
    
    def get_percent_from_stat_rating(self, stat, stat_rating):
        if stat == "Haste":
            return (stat_rating / 170) * 1.04
        if stat == "Crit":
            return (stat_rating / 180)
        if stat == "Mastery":
            return (stat_rating / 120)
        if stat == "Versatility":
            return (stat_rating / 205)
        
    def update_stats_with_racials(self):
        
        # reset stats
        self.spell_power = self.base_spell_power
        self.haste = self.base_haste
        self.crit = self.base_crit
        self.mastery = self.base_mastery
        self.versatility = self.base_versatility
        self.crit_damage_modifier = 1
        self.crit_healing_modifier = 1
        self.max_health = self.base_max_health
        
        # update stats based on race
        if self.race == "Human":
            self.haste = (self.base_haste - 4) * 1.02 + 4
            self.crit = (self.base_crit - 9) * 1.02 + 9
            self.mastery = (self.base_mastery - 6 - 12) * 1.02 + 6 + 12
            self.versatility = self.base_versatility * 1.02
        elif self.race == "Dwarf":
            self.crit_damage_modifier += 0.02
            self.crit_healing_modifier += 0.02
        elif self.race == "Draenei":
            self.spell_power += (113 * 1.05 * 1.04)
        elif self.race == "Lightforged Draenei":
            pass
        elif self.race == "Dark Iron Dwarf":
            pass
        elif self.race == "Blood Elf":
            self.crit = self.base_crit + 1  
        elif self.race == "Tauren":
            self.crit_damage_modifier += 0.02
            self.crit_healing_modifier += 0.02
            self.max_health += 197 * 20
        
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
                            "Word of Glory": WordOfGlory(self),
                            "Aerated Mana Potion": AeratedManaPotion(self),
                            "Elemental Potion of Ultimate Power": ElementalPotionOfUltimatePowerPotion(self),
                            "Potion": Potion(self)
        }     
        
        if self.is_talent_active("Holy Shock"):
            self.abilities["Holy Shock"] = HolyShock(self)
            
        if self.is_talent_active("Divine Toll") and self.is_talent_active("Holy Shock"):
            self.abilities["Divine Toll"] = DivineToll(self)
            
        if self.is_talent_active("Daybreak") and self.is_talent_active("Glimmer of Light") and self.is_talent_active("Holy Shock"):
            self.abilities["Daybreak"] = Daybreak(self)
            
        if self.is_talent_active("Light of Dawn"):
            self.abilities["Light of Dawn"] = LightOfDawn(self)
            
        if self.is_talent_active("Avenging Wrath"):
            self.abilities["Avenging Wrath"] = AvengingWrathSpell(self)
            
        if self.is_talent_active("Divine Favor"):
            self.abilities["Divine Favor"] = DivineFavorSpell(self)
            
        # if self.is_talent_active("Blessing of Freedom"):
        #     self.abilities["Blessing of Freedom"] = BlessingOfFreedomSpell(self)
            
        if self.is_talent_active("Tyr's Deliverance") and self.is_talent_active("Holy Shock"):
            self.abilities["Tyr's Deliverance"] = TyrsDeliveranceSpell(self)
          
        if self.is_talent_active("Light's Hammer"):
            self.abilities["Light's Hammer"] = LightsHammerSpell(self)
            
        if self.is_talent_active("Blessing of Summer"):
            self.abilities["Blessing of the Seasons"] = BlessingOfTheSeasons(self)
            
    def is_talent_active(self, talent_name):
        for row, talents in self.class_talents.items():
            if talent_name in talents and talents[talent_name]["ranks"]["current rank"] > 0:
                return True, talents[talent_name]["ranks"]["current rank"]
        
        for row, talents in self.spec_talents.items():
            if talent_name in talents and talents[talent_name]["ranks"]["current rank"] > 0:
                return True, talents[talent_name]["ranks"]["current rank"]

        return False
    
    # misc simulation functions 
    def update_hasted_cooldowns_with_haste_changes(self):
        for ability in self.abilities.values():
            if ability.hasted_cooldown and ability.original_cooldown is not None:
                elapsed_cooldown = ability.original_cooldown - ability.remaining_cooldown
                ability.remaining_cooldown = ability.calculate_cooldown(self) - elapsed_cooldown * (ability.calculate_cooldown(self) / ability.original_cooldown)
                
    def check_cooldowns(self):
        spell_cooldowns = {}
        
        for ability_name, ability in self.abilities.items():
            spell_cooldowns[ability_name] = {"remaining_cooldown": ability.remaining_cooldown, "base_cooldown": ability.original_cooldown, 
                                             "current_charges": ability.current_charges, "max_charges": ability.max_charges}
            
        return spell_cooldowns
    
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
        if spell_name not in beacon_transfer_rates_single_beacon or spell_name not in beacon_transfer_rates_double_beacon:
            return
        
        beacon_healing = calculate_beacon_healing(spell_name, initial_heal)
        
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
            
    def set_beacon_targets(self, beacon_targets):
        self.beacon_targets = beacon_targets
    
    # handle auras and summons on self
    def apply_summon(self, summon, current_time):
        self.active_summons[summon.name] = summon
        self.events.append(f"{format_time(current_time)}: {summon.name} created: {summon.duration}s")
        summon.apply_effect(self, current_time)
   
    def apply_buff_to_self(self, buff, current_time, stacks_to_apply=1, max_stacks=1, reapply=False):
        # print(f"{buff.name} applied at {current_time}")     
        if buff.name in self.active_auras and not reapply:
            append_aura_applied_event(self.events, f"{self.active_auras[buff.name].name} reapplied", self, self, current_time, self.active_auras[buff.name].duration)
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
    
    def remove_or_decrement_buff_on_self(self, buff, current_time, max_stacks=1):
        if buff.name in self.active_auras:
            if buff.current_stacks > 1:
                buff.current_stacks -= 1
                append_aura_stacks_decremented(self.events, buff.name, self, current_time, buff.current_stacks, duration=self.active_auras[buff.name].duration)
                
                update_self_buff_data(self.self_buff_breakdown, buff.name, current_time, "stacks_decremented", buff.duration, buff.current_stacks)
        else:
            del self.active_auras[buff.name]
            buff.remove_effect(self, current_time)
            append_aura_removed_event(self.events, buff.name, self, self, current_time, duration=self.active_auras[buff.name].duration)
            
            update_self_buff_data(self.self_buff_breakdown, buff.name, current_time, "expired")
    
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
            
            stats_dict = {}
            
            equipment[item_slot] = { "name": item_name, "item level": item_level, "stats": stats_dict, "item ID": item_id }
            # print(f"Item: {item_name}, Slot: {item_slot}, Item Level: {item_level}, Item ID: {item_id}")
            if "stats" in item:
                for stat in item["stats"]:
                    stat_type = stat["type"]["type"].lower()
                    # filter irrelevant stats
                    if stat_type not in ["strength", "agility"]:
                        stat_value = stat["value"]
                        stats_dict[stat_type] = stat_value
                        # print(f" Stat: {stat_type}, Value: {stat_value}")
                        
            enchantments = item.get("enchantments", [])
            item_enchantments = [enchantment["display_string"]["en_GB"] for enchantment in enchantments]
            if item_enchantments:
                equipment[item_slot]["enchantments"] = item_enchantments

            sockets = item.get("sockets", [])
            item_gems = [socket["item"]["name"]["en_GB"] for socket in sockets]
            if item_gems:
                equipment[item_slot]["gems"] = item_gems
                
            # print()

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
                
        # pp.pprint(equipment)
        # print(total_stat_values)
        return equipment
  
    def calculate_stats_from_equipment(self, equipment):
        stat_values_from_equipment = {}
        enchants_from_equipment = []
        gems_from_equipment = []
        bonus_effect_enchants = []
        
        for item_slot, item_data in equipment.items():
            stats = item_data.get("stats", {})
            for stat in stats:
                stat_values_from_equipment[stat] = stat_values_from_equipment.get(stat, 0) + stats[stat]
                
            enchants = item_data.get("enchantments", {})
            for enchant in enchants:
                enchants_from_equipment.append(enchant)
                
            gems = item_data.get("gems", {})
            for gem in gems:
                gems_from_equipment.append(gem)
                
        formatted_enchants = convert_enchants_to_stats(enchants_from_equipment)
        
        return_enchants_stats(self, formatted_enchants, bonus_effect_enchants, stat_values_from_equipment)
        return_gem_stats(self, gems_from_equipment, stat_values_from_equipment)
         
        stat_values_from_equipment["intellect"] += 2089
        # stat_values_from_equipment["intellect"] *= 1.05
        
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
        
        haste_rating_per_percent = 170
        crit_rating_per_percent = 180
        mastery_rating_per_percent = 120
        versatility_rating_per_percent = 205
        
        # 2% haste per point from seal of alacrity, multiplicative
        haste_percent = haste_rating / haste_rating_per_percent
        if self.is_talent_active("Seal of Alacrity") and self.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] == 1:
            haste_percent = haste_percent * 1.02 + 2
        elif self.is_talent_active("Seal of Alacrity") and self.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] == 2:
            haste_percent = haste_percent * 1.04 + 4
            
        # 5% bonus crit
        crit_percent = crit_rating / crit_rating_per_percent + 5
        # 2% crit per point from holy aegis
        if self.is_talent_active("Holy Aegis") and self.class_talents["row5"]["Holy Aegis"]["ranks"]["current rank"] == 1:
            crit_percent += 2
        elif self.is_talent_active("Holy Aegis") and self.class_talents["row5"]["Holy Aegis"]["ranks"]["current rank"] == 2:
            crit_percent += 4
            
        # 12% base mastery
        mastery_percent = mastery_rating / mastery_rating_per_percent + 12
        # 3% mastery per point from seal of might
        if self.is_talent_active("Seal of Might") and self.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 1:
            mastery_percent += 3
        elif self.is_talent_active("Seal of Might") and self.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 2:
            mastery_percent += 6
            
        versatility_percent = versatility_rating / versatility_rating_per_percent
        
        return haste_percent, crit_percent, mastery_percent, versatility_percent
    
    def parse_talents(self, talent_data):
        class_talents = {}
        spec_talents = {}
        active_class_talents = test_active_class_talents
        active_spec_talents = test_active_spec_talents

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
                    
        return Talents(active_class_talents, active_spec_talents)
    

