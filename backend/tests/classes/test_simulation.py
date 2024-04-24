import os
import json
import pprint
import random
import math

from app.classes.simulation import Simulation
from app.classes.paladin import Paladin
from app.classes.target import Target, BeaconOfLight, EnemyTarget
from app.classes.spells_auras import TyrsDeliveranceHeal
from app.classes.auras_buffs import DivinePurpose, BlessingOfDawn, GlimmerOfLightBuff
from app.classes.spells_healing import DivineResonanceHolyShock, RisingSunlightHolyShock, DivineTollHolyShock
from app.main import initialise_simulation, run_simulation
from app.utils.beacon_transfer_rates import beacon_transfer_rates_single_beacon, beacon_transfer_rates_double_beacon

pp = pprint.PrettyPrinter(width=200)

def load_data_from_file(filename):
    with open(filename, "r") as file:
        return json.load(file)

path_to_character_data = os.path.join(os.path.dirname(__file__), "character_data", "character_data.json")
path_to_stats_data = os.path.join(os.path.dirname(__file__), "character_data", "stats_data.json")

path_to_talent_data = os.path.join(os.path.dirname(__file__), "character_data", "talent_data.json")
path_to_base_class_talents_data = os.path.join(os.path.dirname(__file__), "character_data", "base_class_talents")
path_to_base_spec_talents_data = os.path.join(os.path.dirname(__file__), "character_data", "base_spec_talents")

path_to_equipment_data = os.path.join(os.path.dirname(__file__), "character_data", "equipment_data.json")
path_to_updated_equipment_data = os.path.join(os.path.dirname(__file__), "character_data", "updated_equipment_data")

character_data = load_data_from_file(path_to_character_data)
stats_data = load_data_from_file(path_to_stats_data)

talent_data = load_data_from_file(path_to_talent_data)
base_class_talents_data = load_data_from_file(path_to_base_class_talents_data)
base_spec_talents_data = load_data_from_file(path_to_base_spec_talents_data)

equipment_data = load_data_from_file(path_to_equipment_data)
updated_equipment_data = load_data_from_file(path_to_updated_equipment_data)

def initialise_paladin():
    healing_targets = [Target(f"target{i + 1}") for i in range(20)]

    paladin = Paladin("paladin1", character_data, stats_data, talent_data, equipment_data, potential_healing_targets=healing_targets, test=True)
    
    return paladin

def apply_pre_buffs(paladin):
    paladin.apply_consumables()
    paladin.apply_item_effects()
    paladin.apply_buffs_on_encounter_start()
    
def set_up_paladin(paladin):
    paladin.update_equipment(updated_equipment_data)
    apply_pre_buffs(paladin)
    
    targets = paladin.potential_healing_targets
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    return targets, glimmer_targets

def reset_talents(paladin):
    paladin.update_character(class_talents=base_class_talents_data, spec_talents=base_spec_talents_data)
    paladin.update_equipment(updated_equipment_data)
    
def update_talents(paladin, class_talents={}, spec_talents={}):
    paladin.update_character(class_talents=class_talents, spec_talents=spec_talents)
    paladin.update_equipment(updated_equipment_data)

def set_crit_to_max(paladin):
    paladin.flat_crit = 100
    paladin.update_stat("crit", 0)

def test_lights_hammer_hits():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Light's Hammer": 1})
    
    priority_list = ["Light's Hammer"]
    simulation = initialise_simulation(paladin, targets, 20, 1, 0, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation_results = simulation.display_results()
    
    lights_hammer_hits = simulation_results["results"]["ability_breakdown"]["Light's Hammer"]["hits"]
    expected_lights_hammer_hits = 48
    
    assert lights_hammer_hits == expected_lights_hammer_hits
    
def test_lights_hammer_healing():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Light's Hammer": 1})
    
    paladin.crit = -100
    
    priority_list = ["Light's Hammer"]
    simulation = initialise_simulation(paladin, targets, 20, 1, 0, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation.paladin.crit = -100
    
    simulation_results = simulation.display_results()
    lights_hammer_healing = simulation_results["results"]["ability_breakdown"]["Light's Hammer"]["total_healing"] / 48
    expected_lights_hammer_healing = 5600
    
    assert expected_lights_hammer_healing - 200 <= lights_hammer_healing <= expected_lights_hammer_healing + 200, "Light's Hammer healing is outside the expected range"
    
def test_tyrs_deliverance_hits_no_extension():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Tyr's Deliverance": 1})
    
    priority_list = ["Tyr's Deliverance"]
    simulation = initialise_simulation(paladin, targets, 70, 1, 300, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation_results = simulation.display_results()
    
    tyrs_deliverance_hits = simulation_results["results"]["ability_breakdown"]["Tyr's Deliverance"]["hits"]
    tyrs_deliverance_tick_rate = 1 / simulation.paladin.haste_multiplier

    expected_tyrs_deliverance_hits = round(20 / tyrs_deliverance_tick_rate) + 1 + 5
    
    assert tyrs_deliverance_hits == expected_tyrs_deliverance_hits
    
def test_tyrs_deliverance_hits_no_extension_hasted():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Tyr's Deliverance": 1})
    
    priority_list = ["Tyr's Deliverance"]
    simulation = initialise_simulation(paladin, targets, 70, 1, 0, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation_results = simulation.display_results()
    
    tyrs_deliverance_hits = simulation_results["results"]["ability_breakdown"]["Tyr's Deliverance"]["hits"]
    tyrs_deliverance_tick_rate = 1 / (simulation.paladin.haste_multiplier * 1.3)
    
    # accounts for a lower tick rate leading to slightly fewer ticks
    rounded_tick_rate = math.ceil(tyrs_deliverance_tick_rate / simulation.tick_rate + 0.01) * simulation.tick_rate + 0.01

    expected_tyrs_deliverance_hits = round(20 / rounded_tick_rate) + 1 + 5
    
    assert tyrs_deliverance_hits == expected_tyrs_deliverance_hits
    
def test_tyrs_deliverance_hits_with_extension():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Tyr's Deliverance": 1, "Boundless Salvation": 1})
    
    priority_list = ["Tyr's Deliverance", "Holy Light"]
    simulation = initialise_simulation(paladin, targets, 70, 1, 300, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation_results = simulation.display_results()
    
    tyrs_deliverance_hits = simulation_results["results"]["ability_breakdown"]["Tyr's Deliverance"]["hits"]
    tyrs_deliverance_tick_rate = 1 / simulation.paladin.haste_multiplier

    expected_tyrs_deliverance_hits = round(60 / tyrs_deliverance_tick_rate) + 1 + 5
    
    assert tyrs_deliverance_hits == expected_tyrs_deliverance_hits
    
def test_beacon_of_faith_healing():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Afterimage": 1}, {"Light of Dawn": 1, "Beacon of Faith": 1, "Commanding Light": 1, "Resplendent Light": 1, "Glimmer of Light": 1, "Light's Hammer": 1, "Tyr's Deliverance": 1})
    
    priority_list = ["Holy Shock", "Light's Hammer", "Tyr's Deliverance", "Light of Dawn | Holy Power = 5", "Word of Glory | Holy Power = 4", "Daybreak", "Judgment", "Holy Light | Infusion of Light active", "Flash of Light"]
    simulation = initialise_simulation(paladin, targets, 300, 1, 0, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation_results = simulation.display_results()
    
    ability_breakdown = simulation_results["results"]["ability_breakdown"]
    
    beacon_source_spells = ability_breakdown["Beacon of Light"]["source_spells"]
    
    beacon_transfer_ratios = {}
    
    sub_spell_list = {}
    for spell in ability_breakdown:
        for sub_spell in ability_breakdown[spell]["sub_spells"]:
            sub_spell_list[sub_spell] = spell    
    
    for spell in beacon_source_spells:
        if spell in ability_breakdown:
            spell_healing = ability_breakdown[spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
        
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
        if spell in sub_spell_list:
            spell_healing = ability_breakdown[sub_spell_list[spell]]["sub_spells"][spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
            
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
    
    tolerance = 0.05      
     
    for spell in beacon_transfer_ratios:
        assert abs(beacon_transfer_ratios[spell] - beacon_transfer_rates_double_beacon[spell] * 2) <= tolerance
        
def test_beacon_of_virtue_healing():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Afterimage": 1}, {"Light of Dawn": 1, "Commanding Light": 1, "Beacon of Virtue": 1, "Resplendent Light": 1, "Glimmer of Light": 1, "Light's Hammer": 1, "Tyr's Deliverance": 1})
    
    priority_list = ["Beacon of Virtue", "Holy Shock", "Light's Hammer", "Tyr's Deliverance", "Light of Dawn | Holy Power = 5", "Word of Glory | Holy Power = 4", "Daybreak", "Judgment", "Holy Light | Infusion of Light active", "Flash of Light"]
    simulation = initialise_simulation(paladin, targets, 8, 1, 0, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation_results = simulation.display_results()
    
    ability_breakdown = simulation_results["results"]["ability_breakdown"]
    pp.pprint(ability_breakdown)
    
    beacon_source_spells = ability_breakdown["Beacon of Light"]["source_spells"]
    
    beacon_transfer_ratios = {}
    
    sub_spell_list = {}
    for spell in ability_breakdown:
        for sub_spell in ability_breakdown[spell]["sub_spells"]:
            sub_spell_list[sub_spell] = spell    
    
    for spell in beacon_source_spells:
        if spell in ability_breakdown:
            spell_healing = ability_breakdown[spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
        
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
        if spell in sub_spell_list:
            spell_healing = ability_breakdown[sub_spell_list[spell]]["sub_spells"][spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
            
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
    
    tolerance = 0.1    
    
    print(beacon_transfer_ratios)
    for spell in beacon_transfer_ratios:
        assert abs(beacon_transfer_ratios[spell] - beacon_transfer_rates_single_beacon[spell] * 5) <= tolerance
        
def test_beacon_of_virtue_flash_of_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Afterimage": 1}, {"Light of Dawn": 1, "Commanding Light": 1, "Beacon of Virtue": 1, "Resplendent Light": 1, "Glimmer of Light": 1, "Light's Hammer": 1, "Tyr's Deliverance": 1})
    priority_list = ["Beacon of Virtue", "Flash of Light"]
    simulation = initialise_simulation(paladin, targets, 15, 1, 300, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation.paladin.crit = -100
    simulation_results = simulation.display_results()
    
    ability_breakdown = simulation_results["results"]["ability_breakdown"]
    pp.pprint(ability_breakdown)
    
    beacon_source_spells = ability_breakdown["Beacon of Light"]["source_spells"]
    
    beacon_transfer_ratios = {}
    
    sub_spell_list = {}
    for spell in ability_breakdown:
        for sub_spell in ability_breakdown[spell]["sub_spells"]:
            sub_spell_list[sub_spell] = spell    
    
    for spell in beacon_source_spells:
        if spell in ability_breakdown:
            spell_healing = ability_breakdown[spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
        
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
        if spell in sub_spell_list:
            spell_healing = ability_breakdown[sub_spell_list[spell]]["sub_spells"][spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
            
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
    
    tolerance = 0.05
    
    # 5 out of 11 casts completed during virtue window    
    for spell in beacon_transfer_ratios:
        assert abs(beacon_transfer_ratios[spell] - beacon_transfer_rates_single_beacon[spell] * 5 * (5 / 11)) <= tolerance
   
def test_beacon_of_virtue_flash_of_light_multiple_virtue_casts():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Afterimage": 1}, {"Light of Dawn": 1, "Commanding Light": 1, "Beacon of Virtue": 1, "Resplendent Light": 1, "Glimmer of Light": 1, "Light's Hammer": 1, "Tyr's Deliverance": 1})
    priority_list = ["Beacon of Virtue", "Flash of Light"]
    simulation = initialise_simulation(paladin, targets, 45, 1, 300, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation.paladin.crit = -100
    simulation_results = simulation.display_results()
    
    ability_breakdown = simulation_results["results"]["ability_breakdown"]
    pp.pprint(ability_breakdown)
    
    beacon_source_spells = ability_breakdown["Beacon of Light"]["source_spells"]
    
    beacon_transfer_ratios = {}
    
    sub_spell_list = {}
    for spell in ability_breakdown:
        for sub_spell in ability_breakdown[spell]["sub_spells"]:
            sub_spell_list[sub_spell] = spell    
    
    for spell in beacon_source_spells:
        if spell in ability_breakdown:
            spell_healing = ability_breakdown[spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
        
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
        if spell in sub_spell_list:
            spell_healing = ability_breakdown[sub_spell_list[spell]]["sub_spells"][spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
            
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
    
    tolerance = 0.05
    
    print(beacon_transfer_ratios)
    # 5 out of 11 casts completed during virtue window    
    for spell in beacon_transfer_ratios:
        assert abs(beacon_transfer_ratios[spell] - beacon_transfer_rates_single_beacon[spell] * 5 * (15 / 34)) <= tolerance     
    
def test_beacon_of_virtue_lights_hammer():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Afterimage": 1}, {"Light of Dawn": 1, "Beacon of Virtue": 1, "Resplendent Light": 1, "Glimmer of Light": 1, "Light's Hammer": 1, "Tyr's Deliverance": 1})
    priority_list = ["Beacon of Virtue", "Light's Hammer"]
    simulation = initialise_simulation(paladin, targets, 20, 1, 0, priority_list, updated_equipment_data, tick_rate=0.05, raid_health=0.7, mastery_effectiveness=95, light_of_dawn_targets=5, lights_hammer_targets=6, resplendent_light_targets=5, test=True)
    simulation.paladin.crit = -100
    simulation_results = simulation.display_results()
    
    ability_breakdown = simulation_results["results"]["ability_breakdown"]
    pp.pprint(ability_breakdown)
    
    beacon_source_spells = ability_breakdown["Beacon of Light"]["source_spells"]
    
    beacon_transfer_ratios = {}
    
    sub_spell_list = {}
    for spell in ability_breakdown:
        for sub_spell in ability_breakdown[spell]["sub_spells"]:
            sub_spell_list[sub_spell] = spell    
    
    for spell in beacon_source_spells:
        if spell in ability_breakdown:
            spell_healing = ability_breakdown[spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
        
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
        if spell in sub_spell_list:
            spell_healing = ability_breakdown[sub_spell_list[spell]]["sub_spells"][spell]["total_healing"]
            beacon_healing = beacon_source_spells[spell]["healing"]
            
            beacon_transfer_ratios[spell] = round(beacon_healing / spell_healing, 3)
    
    tolerance = 0.05
    
    print(beacon_transfer_ratios)
    # 6.8 out of 14 seconds spent during virtue 
    for spell in beacon_transfer_ratios:
        assert abs(beacon_transfer_ratios[spell] - beacon_transfer_rates_single_beacon[spell] * 5 * (6.8 / 14)) <= tolerance            