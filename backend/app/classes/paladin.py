import pprint

from ..utils.misc_functions import format_time, append_aura_applied_event, append_aura_removed_event, append_aura_stacks_decremented
from .spells import Wait
from .spells_healing import HolyShock, WordOfGlory, LightOfDawn, FlashOfLight, HolyLight, DivineToll, Daybreak, LightsHammerSpell
from .spells_damage import Judgment, CrusaderStrike
from .spells_auras import AvengingWrathSpell, DivineFavorSpell, BlessingOfFreedomSpell, TyrsDeliveranceSpell, BlessingOfTheSeasons
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
    
    def __init__(self, name, character_data=None, stats_data=None, talent_data=None, equipment_data=None, buffs=None, potential_healing_targets=None):
        self.character_data = character_data if character_data else None
        self.race = self.character_data["race"]["name"] if self.character_data else None
        self.name = name[0].upper() + name[1:]
        # self.stats = self.parse_stats(stats_data)
        # self.class_talents = self.parse_talents(talent_data)[0]
        # self.spec_talents = self.parse_talents(talent_data)[1]
        
        # self.talents = self.parse_talents(talent_data)
        # self.class_talents = self.talents.class_talents
        # self.spec_talents = self.talents.spec_talents
        
        # self.class_talents = self.parse_talents(talent_data)
        # self.spec_talents = self.parse_talents(talent_data)
        
        # self.talents = self.parse_talents(talent_data)
        self.class_talents = test_active_class_talents
        self.spec_talents = test_active_spec_talents

        # self.class_talents["row8"]["Seal of Alacrity"]["ranks"]["current rank"] = 0
        # print(self.class_talents["row3"]["Greater Judgment"])
        
        self.base_mana = 250000
        self.mana = self.base_mana
        self.max_mana = self.base_mana
        self.mana_regen_per_second = 2000
        
        if equipment_data:
            self.equipment = self.parse_equipment(equipment_data)
            formatted_equipment_data = self.calculate_stats_from_equipment(self.equipment)
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
            print(self.haste, self.crit, self.mastery, self.versatility)
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
        
        self.haste_multiplier = (self.haste / 100) + 1
        self.crit_multiplier = (self.crit / 100) + 1
        self.mastery_multiplier = (self.mastery / 100) + 1
        self.versatility_multiplier = (self.versatility / 100) + 1
        # print(self.haste_multiplier, self.crit_multiplier, self.mastery_multiplier, self.versatility_multiplier)
        
        self.mastery_effectiveness = 1
    
        self.buffs = buffs
        
        self.base_global_cooldown = 1.5
        self.hasted_global_cooldown = self.base_global_cooldown / self.haste_multiplier
        self.global_cooldown = 0
        
        self.abilities = {
                            "Wait": Wait(),
                            "Flash of Light": FlashOfLight(self),
                            "Holy Light": HolyLight(self),
                            "Crusader Strike": CrusaderStrike(self),
                            "Judgment": Judgment(self),
                            "Word of Glory": WordOfGlory(self),
        }      
        self.load_abilities_based_on_talents()
        
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
        
        # for reclamation
        self.average_raid_health_percentage = 1
    
    def update_hasted_cooldowns_with_haste_changes(self):
        for ability in self.abilities.values():
            if ability.hasted_cooldown and ability.original_cooldown is not None:
                elapsed_cooldown = ability.original_cooldown - ability.remaining_cooldown
                ability.remaining_cooldown = ability.calculate_cooldown(self) - elapsed_cooldown * (ability.calculate_cooldown(self) / ability.original_cooldown)
    
    def load_abilities_based_on_talents(self):
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
            
        if self.is_talent_active("Blessing of Freedom"):
            self.abilities["Blessing of Freedom"] = BlessingOfFreedomSpell(self)
            
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
    
    def get_effective_spell_power(self):
        spell_power = self.spell_power
        if self.is_talent_active("Seal of Might") and self.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 1:
            return spell_power * 1.02
        elif self.is_talent_active("Seal of Might") and self.class_talents["row8"]["Seal of Might"]["ranks"]["current rank"] == 2:
            return spell_power * 1.04
        return spell_power
            
    def receive_self_heal(self, amount):
        self.self_healing += amount
   
    def apply_summon(self, summon, current_time):
        self.active_summons[summon.name] = summon
        self.events.append(f"{format_time(current_time)}: {summon.name} created: {summon.duration}s")
        summon.apply_effect(self, current_time)
   
    def apply_buff_to_self(self, buff, current_time, stacks_to_apply=1, max_stacks=1):
        # print(f"{buff.name} applied at {current_time}")     
        if buff.name in self.active_auras:
            if buff.current_stacks < max_stacks:
                buff.current_stacks += stacks_to_apply
                buff.duration = buff.base_duration
            self.active_auras[buff.name] = buff
        else:
            self.active_auras[buff.name] = buff
            buff.apply_effect(self)
        
        append_aura_applied_event(self.events, buff.name, self, self, current_time, self.active_auras[buff.name].duration, buff.current_stacks, max_stacks)
        # print(f"new crit %: {self.crit}")
        
    def extend_buff_on_self(self, buff, current_time, time_extension):
        if buff.name in self.active_auras:
            self.active_auras[buff.name].duration += time_extension
            self.events.append(f"{format_time(current_time)}: {buff.name} extended by {time_extension}s to {round(self.active_auras[buff.name].duration, 2)}s")
    
    def remove_or_decrement_buff_on_self(self, buff, current_time, max_stacks=1):
        if buff.name in self.active_auras:
            if buff.current_stacks > 1:
                buff.current_stacks -= 1
                append_aura_stacks_decremented(self.events, buff.name, self, current_time, buff.current_stacks, duration=self.active_auras[buff.name].duration)
        else:
            del self.active_auras[buff.name]
            buff.remove_effect(self)
            append_aura_removed_event(self.events, buff.name, self, self, current_time, duration=self.active_auras[buff.name].duration)
        
    def set_beacon_targets(self, beacon_targets):
        self.beacon_targets = beacon_targets
    
    def update_gcd(self, tick_rate):     
        self.hasted_global_cooldown = self.base_global_cooldown / self.haste_multiplier
           
        if self.global_cooldown > 0:
            self.global_cooldown = max(0, self.global_cooldown - tick_rate)
        
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
        stat_values_from_equipment["intellect"] *= 1.05
        
        stat_values_from_equipment["stamina"] += 3848
        if self.is_talent_active("Sanctified Plates") and self.class_talents["row6"]["Sanctified Plates"]["ranks"]["current rank"] == 1:
            stat_values_from_equipment["stamina"] *= 1.03
        elif self.is_talent_active("Sanctified Plates") and self.class_talents["row6"]["Sanctified Plates"]["ranks"]["current rank"] == 2:
            stat_values_from_equipment["stamina"] *= 1.06
        
        if self.race == "Human":
            stat_values_from_equipment["haste"] *= 1.02
            stat_values_from_equipment["crit"] *= 1.02
            stat_values_from_equipment["mastery"] *= 1.02
            stat_values_from_equipment["versatility"] *= 1.02
        
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
    

