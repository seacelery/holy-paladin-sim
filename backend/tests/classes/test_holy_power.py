import os
import json
import pprint

from app.classes.paladin import Paladin
from app.classes.target import Target, BeaconOfLight, EnemyTarget
from app.classes.spells import Spell
from app.classes.spells_healing import HolyShock, HolyLight, FlashOfLight, DivineToll, DivineResonanceHolyShock, RisingSunlightHolyShock
from app.classes.spells_damage import Judgment, CrusaderStrike
from app.classes.auras_buffs import DivinePurpose

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

    paladin = Paladin("paladin1", character_data, stats_data, talent_data, equipment_data, potential_healing_targets=healing_targets)
    
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
    
def test_holy_power_cap():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    paladin.holy_power = 5
    holy_shock = paladin.abilities["Holy Shock"]
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_holy_power = 5
    assert paladin.holy_power == expected_holy_power, "Holy Power overcapped"
    
def test_holy_shock():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    holy_shock = paladin.abilities["Holy Shock"]
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_holy_power = 1
    assert paladin.holy_power == expected_holy_power, "Holy Shock holy power unexpected value"
    
def test_holy_shock_rising_sunlight():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Rising Sunlight": 1}, {})
    
    rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
    
    target = [targets[0]]
    _, _, _, _, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_holy_power = 1
    assert paladin.holy_power == expected_holy_power, "Holy Shock (Rising Sunlight) holy power unexpected value"
    
def test_holy_shock_divine_resonance():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Resonance": 1}, {})
    
    divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
    
    target = [targets[0]]
    _, _, _, _, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_holy_power = 1
    assert paladin.holy_power == expected_holy_power, "Holy Shock (Divine Resonance) holy power unexpected value"
    
def test_divine_toll():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Toll": 1, "Divine Resonance": 1}, {})
    
    divine_toll = paladin.abilities["Divine Toll"]
    
    target = [targets[0]]
    _, _, _ = divine_toll.cast_healing_spell(paladin, target, 0, False, glimmer_targets)
    
    expected_holy_power = 5
    assert paladin.holy_power == expected_holy_power, "Divine Toll holy power unexpected value"
    assert "Divine Resonance" in paladin.active_auras
    
def test_holy_light():
    # no talents
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    holy_light = paladin.abilities["Holy Light"]
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 0
    assert paladin.holy_power == expected_holy_power, "Holy Light holy power unexpected value"
    
def test_holy_light_tower_of_radiance():
    # tower of radiance
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Tower of Radiance": 1})
    
    holy_light = paladin.abilities["Holy Light"]
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 1
    assert paladin.holy_power == expected_holy_power, "Holy Light (Tower of Radiance) holy power unexpected value"
    
def test_holy_light_tower_of_radiance_infusion_of_light():
    # tower of radiance & infusion of light
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Tower of Radiance": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    holy_light = paladin.abilities["Holy Light"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.holy_power = 0
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 3
    assert paladin.holy_power == expected_holy_power, "Holy Light (Tower of Radiance & Infusion of Light) holy power unexpected value"
    
def test_holy_light_tower_of_radiance_infusion_of_light_inflorescence_of_the_sunwell():
    # tower of radiance & infusion of light /w inflorescence of the sunwell
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Tower of Radiance": 1, "Inflorescence of the Sunwell": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    holy_light = paladin.abilities["Holy Light"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    # holy shock 1 for 2 infusion stacks
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.holy_power = 0
    
    # holy light 1 for 3 holy power
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    expected_holy_power = 3
    assert paladin.holy_power == expected_holy_power, "Holy Light (Tower of Radiance & Infusion of Light /w Inflorescence of the Sunwell) holy power unexpected value"
    paladin.global_cooldown = 0
    paladin.holy_power = 0
    
    # holy light 2 for 3 holy power
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    expected_holy_power = 3
    assert paladin.holy_power == expected_holy_power, "Holy Light (Tower of Radiance & Infusion of Light /w Inflorescence of the Sunwell) holy power unexpected value"
    paladin.global_cooldown = 0
    paladin.holy_power = 0
    
    # holy shock 2 for 2 infusion stacks
    holy_shock.remaining_cooldown = 0
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.holy_power = 0
    
    # holy light 3 for 4 holy power
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    expected_holy_power = 4
    assert paladin.holy_power == expected_holy_power, "Holy Light (Tower of Radiance & Infusion of Light /w Inflorescence of the Sunwell) holy power unexpected value"
    
def test_flash_of_light():
    # no talents
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    flash_of_light = paladin.abilities["Flash of Light"]
    
    target = [targets[0]]
    _, _, _ , _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 0
    assert paladin.holy_power == expected_holy_power, "Flash of Light holy power unexpected value"
    
def test_flash_of_light_tower_of_radiance():
    # tower of radiance
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Tower of Radiance": 1})
    
    flash_of_light = paladin.abilities["Flash of Light"]
    
    target = [targets[0]]
    _, _, _ , _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 1
    assert paladin.holy_power == expected_holy_power, "Flash of Light (Tower of Radiance) holy power unexpected value"
    
def test_judgment():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    judgment = paladin.abilities["Judgment"]
    
    target = [targets[0]]
    _, _, _, _, _, _ = judgment.cast_damage_spell(paladin, [EnemyTarget("enemyTarget1")], 0, True)
    
    expected_holy_power = 1
    assert paladin.holy_power == expected_holy_power, "Judgment holy power unexpected value"
    
def test_crusader_strike():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    crusader_strike = paladin.abilities["Crusader Strike"]
    
    target = [targets[0]]
    _, _, _, _ = crusader_strike.cast_damage_spell(paladin, [EnemyTarget("enemyTarget1")], 0, True)
    
    expected_holy_power = 1
    assert paladin.holy_power == expected_holy_power, "Crusader Strike holy power unexpected value"
    
def test_crusader_strike_holy_infusion():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Holy Infusion": 1})
    
    crusader_strike = paladin.abilities["Crusader Strike"]
    
    target = [targets[0]]
    _, _, _, _ = crusader_strike.cast_damage_spell(paladin, [EnemyTarget("enemyTarget1")], 0, True)
    
    expected_holy_power = 2
    assert paladin.holy_power == expected_holy_power, "Crusader Strike (Holy Infusion) holy power unexpected value"
    
def test_word_of_glory():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.holy_power = 3
    _, _, _, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 0
    assert paladin.holy_power == expected_holy_power, "Word of Glory holy power unexpected value"
    
def test_word_of_glory_divine_purpose():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.holy_power = 3
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, _, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 3
    assert paladin.holy_power == expected_holy_power, "Word of Glory (Divine Purpose) holy power unexpected value"
    
def test_light_of_dawn():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.holy_power = 3
    _, _, _, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 0
    assert paladin.holy_power == expected_holy_power, "Light of Dawn holy power unexpected value"
    
def test_light_of_dawn_divine_purpose():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.holy_power = 3
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, _, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_holy_power = 3
    assert paladin.holy_power == expected_holy_power, "Light of Dawn (Divine Purpose) holy power unexpected value"