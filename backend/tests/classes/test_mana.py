import os
import json
import pprint

from app.classes.paladin import Paladin
from app.classes.target import Target, BeaconOfLight, EnemyTarget
from app.classes.spells import Spell
from app.classes.spells_auras import TyrsDeliveranceSpell, TyrsDeliveranceHeal
from app.classes.spells_healing import HolyShock, HolyLight, FlashOfLight
from app.classes.spells_damage import Judgment
from app.classes.auras_buffs import TyrsDeliveranceTargetBuff, DivinePurpose, Innervate

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

def test_divine_revelations():
    # holy light
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Divine Revelations": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    holy_light = paladin.abilities["Holy Light"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.crit = -100
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    divine_revelations_mana_gain = 1312.5
    remaining_mana = 262500 - 7000 - 6000
    assert remaining_mana + divine_revelations_mana_gain == paladin.mana, "Holy Light (Divine Revelations) mana gain incorrect"
    
    #judgment
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Divine Revelations": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    judgment = paladin.abilities["Judgment"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    _, _, _, _, _ = judgment.cast_damage_spell(paladin, [EnemyTarget("enemyTarget1")], 0, True)
    
    divine_revelations_mana_gain = 1312.5
    expected_remaining_mana = 262500 - 7000 - 6000 + divine_revelations_mana_gain
    assert expected_remaining_mana == paladin.mana, "Judgment (Divine Revelations) mana gain incorrect"
    
# Divine Favour's mana reduction is bugged for Flash of Light
# def test_flash_of_light_divine_favor():     
#     paladin = initialise_paladin()
#     targets, glimmer_targets = set_up_paladin(paladin)
    
#     reset_talents(paladin)
#     update_talents(paladin, {}, {"Divine Favor": 1})
    
#     divine_favor = paladin.abilities["Divine Favor"]
#     flash_of_light = paladin.abilities["Flash of Light"]
    
#     paladin.crit = -100
    
#     target = [targets[0]]
#     _, _, _ = divine_favor.cast_healing_spell(paladin, target, 0, False)
#     _, _, _ , _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
#     expected_remaining_mana = 262500 - 4500
#     calculated_remaining_mana = paladin.max_mana - flash_of_light.base_mana_cost * paladin.base_mana * 0.5
    
#     assert expected_remaining_mana == paladin.mana, "Flash of Light (Divine Favor) mana reduction incorrect"
#     assert calculated_remaining_mana == paladin.mana, "Flash of Light (Divine Favor) mana reduction incorrect"
    
def test_holy_light_divine_favor():     
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Divine Favor": 1})
    
    divine_favor = paladin.abilities["Divine Favor"]
    holy_light = paladin.abilities["Holy Light"]
    
    paladin.crit = -100
    
    target = [targets[0]]
    _, _, _ = divine_favor.cast_healing_spell(paladin, target, 0, False)
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_remaining_mana = 262500 - 3000
    calculated_remaining_mana = paladin.max_mana - holy_light.base_mana_cost * paladin.base_mana * 0.5
    
    assert expected_remaining_mana == paladin.mana, "Holy Light (Divine Favor) mana reduction incorrect"
    assert calculated_remaining_mana == paladin.mana, "Holy Light (Divine Favor) mana reduction incorrect"
 
def test_flash_of_light_infusion_of_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    holy_shock = paladin.abilities["Holy Shock"]
    flash_of_light = paladin.abilities["Flash of Light"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.crit = -100
    _, _, _ , _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_remaining_mana = 262500 - 2700 - 7000
    calculated_remaining_mana = paladin.max_mana - flash_of_light.base_mana_cost * paladin.base_mana * 0.3 - holy_shock.base_mana_cost * paladin.base_mana
    
    assert expected_remaining_mana == paladin.mana, "Flash of Light (Infusion of Light) mana reduction incorrect"
    assert calculated_remaining_mana == paladin.mana, "Flash of Light (Infusion of Light) mana reduction incorrect" 
    
def test_flash_of_light_infusion_of_light_inflorescence_of_the_sunwell():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Inflorescence of the Sunwell": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    flash_of_light = paladin.abilities["Flash of Light"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.crit = -100
    _, _, _ , _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_remaining_mana = 262500 - 7000
    calculated_remaining_mana = paladin.max_mana - flash_of_light.base_mana_cost * paladin.base_mana * 0 - holy_shock.base_mana_cost * paladin.base_mana
    
    assert expected_remaining_mana == paladin.mana, "Flash of Light (Infusion of Light, Inflorescence of the Sunwell) mana reduction incorrect"
    assert calculated_remaining_mana == paladin.mana, "Flash of Light (Infusion of Light, Inflorescence of the Sunwell) mana reduction incorrect"
    
def test_divine_purpose():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1}, {"Light of Dawn": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    
    target = [targets[0]]
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, _, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, _, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_remaining_mana = 262500
    
    assert expected_remaining_mana == paladin.mana, "Divine Purpose mana reduction incorrect"
    
def test_innervate():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    holy_light = paladin.abilities["Holy Light"]
    flash_of_light = paladin.abilities["Flash of Light"]
    word_of_glory = paladin.abilities["Word of Glory"]
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.apply_buff_to_self(Innervate(), 0)
    paladin.holy_power = 3
    _, _, _, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    paladin.holy_power = 3
    _, _, _, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _ , _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, _ , _ = holy_light.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_remaining_mana = 262500
    
    assert expected_remaining_mana == paladin.mana, "Innervate mana reduction incorrect"
    
def test_reclamation():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Reclamation": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    crusader_strike = paladin.abilities["Crusader Strike"]
    
    # 70% health means we expect 3% mana refund
    paladin.average_raid_health_percentage = 0.7
    
    target = [targets[0]]
    _, _, _, _ , _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_remaining_mana = 262500 - 7000 + (7000 * 0.03)
    assert expected_remaining_mana == paladin.mana, "Holy Shock (Reclamation) mana reduction incorrect"
    
    paladin.global_cooldown = 0
    _, _, _, _ = crusader_strike.cast_damage_spell(paladin, [EnemyTarget("enemyTarget1")], 0, True)
    
    expected_remaining_mana = expected_remaining_mana - 1500 + (1500 * 0.03)
    assert expected_remaining_mana == paladin.mana, "Crusader Strike (Reclamation) mana reduction incorrect"