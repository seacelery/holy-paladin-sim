import os
import json
import pprint
import random
import math

from app.classes.paladin import Paladin
from app.classes.target import Target, BeaconOfLight, EnemyTarget
from app.classes.spells_auras import TyrsDeliveranceHeal
from app.classes.auras_buffs import DivinePurpose, BlessingOfDawn, GlimmerOfLightBuff, AvengingWrathBuff, BlessingOfSpring, TimeWarp, BlessingOfAutumn
from app.classes.spells_healing import DivineResonanceHolyShock, RisingSunlightHolyShock, DivineTollHolyShock
from app.classes.spells_passives import TouchOfLight

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
    healing_targets = [Target(f"target{i + 1}") for i in range(18)] + [BeaconOfLight(f"beaconTarget{i + 1}") for i in range(2)]
    beacon_targets = [target for target in healing_targets if isinstance(target, BeaconOfLight)]

    paladin = Paladin("daisu", character_data, stats_data, talent_data, equipment_data, potential_healing_targets=healing_targets)
    paladin.set_beacon_targets(beacon_targets)
    
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
    
def test_hasted_cooldown():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    holy_shock = paladin.abilities["Holy Shock"]
    
    paladin.crit = -100
    
    target = [targets[0]]
    _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_cooldown = round(8.5 / 1.2548, 2)
    holy_shock_cooldown = holy_shock.remaining_cooldown

    assert round(holy_shock_cooldown, 2) == expected_cooldown, "Holy Shock unexpected cooldown value"
    
def test_hasted_cooldown_update():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    holy_shock = paladin.abilities["Holy Shock"]
    
    paladin.crit = -100
    
    target = [targets[0]]
    _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.apply_buff_to_self(TimeWarp(), 0)
    
    expected_cooldown = round((8.5 / 1.2548) / 1.3, 2)
    holy_shock_cooldown = holy_shock.remaining_cooldown

    assert round(holy_shock_cooldown, 2) == expected_cooldown, "Holy Shock unexpected cooldown value"
    
def test_imbued_infusions():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light's Conviction": 1, "Imbued Infusions": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    holy_light = paladin.abilities["Holy Light"]
    flash_of_light = paladin.abilities["Flash of Light"]
    judgment = paladin.abilities["Judgment"]
    
    set_crit_to_max(paladin)
    
    # holy light
    target = [targets[0]]
    _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    _, _, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_cooldown = round(8.5 / 1.2548, 2) - 2
    holy_shock_cooldown = holy_shock.remaining_cooldown

    assert round(holy_shock_cooldown, 2) == expected_cooldown, "Holy Shock unexpected cooldown value"
    
    # flash of light
    holy_shock.remaining_cooldown = 0
    paladin.global_cooldown = 0
    _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    _, _, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_cooldown = round(8.5 / 1.2548, 2) - 2
    holy_shock_cooldown = holy_shock.remaining_cooldown

    assert round(holy_shock_cooldown, 2) == expected_cooldown, "Holy Shock unexpected cooldown value"
    
    # judgment
    holy_shock.remaining_cooldown = 0
    paladin.global_cooldown = 0
    _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    _, _, _, _, _ = judgment.cast_damage_spell(paladin, [EnemyTarget("enemyTarget1")], 0, True)
    
    expected_cooldown = round(8.5 / 1.2548, 2) - 2
    holy_shock_cooldown = holy_shock.remaining_cooldown

    assert round(holy_shock_cooldown, 2) == expected_cooldown, "Holy Shock unexpected cooldown value"
    
def test_imbued_infusions_charge_overlap():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light's Conviction": 1, "Imbued Infusions": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    holy_light = paladin.abilities["Holy Light"]
    
    set_crit_to_max(paladin)
    
    # holy light
    target = [targets[0]]
    holy_shock.current_charges = 1
    _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    holy_shock.remaining_cooldown = 1.5
    paladin.global_cooldown = 0
    _, _, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_charges = 1
    expected_cooldown = round(8.5 / 1.2548, 2) - 0.5
    holy_shock_charges = holy_shock.current_charges
    holy_shock_cooldown = holy_shock.remaining_cooldown

    assert holy_shock.max_charges == 2
    assert holy_shock_charges == expected_charges
    assert round(holy_shock_cooldown, 2) == expected_cooldown, "Holy Shock unexpected cooldown value"
    
