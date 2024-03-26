import os
import json
import pprint
import random
import math

from app.classes.paladin import Paladin
from app.classes.target import Target, BeaconOfLight, EnemyTarget
from app.classes.spells_auras import TyrsDeliveranceHeal
from app.classes.auras_buffs import DivinePurpose, BlessingOfDawn, GlimmerOfLightBuff, AvengingWrathBuff, BlessingOfSpring, AvengingWrathAwakening
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
    

# heals
def test_holy_shock():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (no talents, no crit) unexpected value"
    
def test_holy_shock_reclamation():        
    # no talents, no crit, reclamation at 70%
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Reclamation": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        paladin.average_raid_health_percentage = 0.7
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(17980 * 1.15 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (no talents, no crit, Reclamation at 70%) unexpected value"
    
def test_holy_shock_crit():
    # no talents - crit & infusion of light application
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980 * 2
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (no talents, crit) unexpected value"
        assert "Infusion of Light" in paladin.active_auras
    
def test_holy_shock_awestruck():
    # awestruck - no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round((17980) / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (Awestruck, no crit) unexpected value"
    
    # awestruck - crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round((17980 * 2 * 1.1) / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (Awestruck, crit) unexpected value"
        
def test_holy_shock_tyrs_deliverance():   
    # tyr's deliverance, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Tyr's Deliverance": 1})
        
        tyrs_deliverance = TyrsDeliveranceHeal(paladin)
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = tyrs_deliverance.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(17980 * 1.15 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (Tyr's Deliverance, no crit) unexpected value"
        
def test_holy_shock_crit_chance():
    # no talents
    iterations = 10000
    crits = 0
    
    for _ in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        target = [targets[0]]
        _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        if heal_crit:
            crits += 1
            
    holy_shock_bonus_crit = 0.1
            
    expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
    # divine glimpse
    iterations = 10000
    crits = 0
    
    for _ in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Divine Glimpse": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        target = [targets[0]]
        _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        if heal_crit:
            crits += 1
            
    holy_shock_bonus_crit = 0.1
    divine_glimpse_bonus_crit = 0.08
            
    expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit + divine_glimpse_bonus_crit
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (divine glimpse)"
    
def test_divine_resonance_holy_shock():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Divine Resonance Holy Shock (no talents, no crit) unexpected value"
        
def test_divine_toll_holy_shock():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        divine_resonance_toll = DivineTollHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = divine_resonance_toll.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Divine Toll Holy Shock (no talents, no crit) unexpected value"
        
def test_rising_sunlight_holy_shock():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
        
        paladin.crit = -10
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = 17980
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Rising Sunlight Holy Shock (no talents, no crit) unexpected value"
    
def test_holy_light():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (no talents, no crit) unexpected value"
        
def test_holy_light_resplendent_light():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Resplendent Light": 1})
        
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, resplendent_light_heal_amount, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 * 0.08 / 10) * 10
        assert round(resplendent_light_heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (no talents, no crit) unexpected value"
        
def test_holy_light_crit():        
    # no talents, crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_light = paladin.abilities["Holy Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 * 2 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (no talents, crit) unexpected value"
   
def test_holy_light_awestruck():     
    # awestruck, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Awestruck, no crit) unexpected value"
        
    # awestruck, crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        holy_light = paladin.abilities["Holy Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 * 2 * 1.1 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Awestruck, no crit) unexpected value"
        
def test_holy_light_divine_favor():     
    # divine favour, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Divine Favor": 1})
        
        divine_favor = paladin.abilities["Divine Favor"]
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = divine_favor.cast_healing_spell(paladin, target, 0, False)
        divine_favor_cast_time = holy_light.calculate_cast_time(paladin)
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 * 1.6 / 10) * 10
        expected_cast_time = 1.39
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Divine Favor, no crit) unexpected value"
        assert round(divine_favor_cast_time, 2) == expected_cast_time
        
def test_holy_light_hand_of_divinity():     
    # hand_of_divinity, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Hand of Divinity": 1})
        
        hand_of_divinity = paladin.abilities["Hand of Divinity"]
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = hand_of_divinity.cast_healing_spell(paladin, target, 0, False)
        paladin.global_cooldown = 0
        hand_of_divinity_cast_time = holy_light.calculate_cast_time(paladin)
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 * 1.4 / 10) * 10
        expected_cast_time = 0
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Hand of Divinity, no crit) unexpected value"
        assert round(hand_of_divinity_cast_time, 2) == expected_cast_time
    
def test_holy_light_tyrs_deliverance():   
    # tyr's deliverance, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Tyr's Deliverance": 1})
        
        tyrs_deliverance = TyrsDeliveranceHeal(paladin)
        holy_light = paladin.abilities["Holy Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = tyrs_deliverance.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0
        _, _, heal_amount, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(59692 * 1.15 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Light (Tyr's Deliverance, no crit) unexpected value"
    
def test_flash_of_light():
    # no talents, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(46210 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (no talents, no crit) unexpected value"
        
def test_flash_of_light_crit():        
    # no talents, crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(46210 * 2 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (no talents, crit) unexpected value"
   
def test_flash_of_light_awestruck():     
    # awestruck, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(46210 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Awestruck, no crit) unexpected value"
        
    # awestruck, crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Awestruck": 1})
        
        flash_of_light = paladin.abilities["Flash of Light"]
        
        set_crit_to_max(paladin)
        
        target = [targets[0]]
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(46210 * 2 * 1.1 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Awestruck, no crit) unexpected value"
        
def test_flash_of_light_divine_favor():     
    # divine favour, no crit & flash of light cast time
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Divine Favor": 1})
        
        divine_favor = paladin.abilities["Divine Favor"]
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = divine_favor.cast_healing_spell(paladin, target, 0, False)
        divine_favor_cast_time = flash_of_light.calculate_cast_time(paladin)
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(46210 * 1.6 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Divine Favor, no crit) unexpected value"
        assert round(divine_favor_cast_time / 0.01) * 0.01 == 0.84
    
def test_flash_of_light_tyrs_deliverance():   
    # tyr's deliverance, no crit
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Tyr's Deliverance": 1})
        
        tyrs_deliverance = TyrsDeliveranceHeal(paladin)
        flash_of_light = paladin.abilities["Flash of Light"]
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, _ = tyrs_deliverance.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0
        _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
        
        expected_heal_amount = round(46210 * 1.15 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Tyr's Deliverance, no crit) unexpected value"
        
def test_flash_of_light_divine_revelations():
    # divine revelations, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Divine Revelations": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    flash_of_light = paladin.abilities["Flash of Light"]
    
    set_crit_to_max(paladin)
    
    target = [targets[0]]
    _, _, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.crit = -100
    _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(46210 * 1.2 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Divine Revelations, no crit) unexpected value"
    
def test_flash_of_light_moment_of_compassion():
    # moment of compassion, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Moment of Compassion": 1, "Beacon of Faith": 1})
    paladin.set_beacon_targets()
    
    flash_of_light = paladin.abilities["Flash of Light"]
    
    set_crit_to_max(paladin)
    target = [random.choice(paladin.beacon_targets)]
    paladin.crit = -100
    _, _, heal_amount, _ = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(46210 * 1.15 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Flash of Light (Moment of Compassion, no crit) unexpected value"
    
def test_word_of_glory():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(40587 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Word of Glory (no talents, no crit) unexpected value"
    
def test_word_of_glory_divine_purpose():
    # divine purpose, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(40587 * 1.15 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Word of Glory (Divine Purpose, no crit) unexpected value"
    
def test_word_of_glory_blessing_of_dawn():
    # blessing of dawn, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Of Dusk and Dawn": 1}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(BlessingOfDawn(), 0)
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(40587 * 1.3 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Word of Glory (Of Dusk and Dawn, no crit) unexpected value"
    
def test_word_of_glory_unending_light():
    # unending light, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Unending Light": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(40587 * 1.45 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Word of Glory (Unending Light - 9 stacks, no crit) unexpected value"
    
def test_word_of_glory_healing_modifier_reset():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1, "Of Dusk and Dawn": 1}, {"Light of Dawn": 1, "Unending Light": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    paladin.apply_buff_to_self(BlessingOfDawn(), 0)
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(40587 * 1.45 * 1.3 * 1.15 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Word of Glory (Unending Light - 9 stacks, Divine Purpose, Blessing of Dawn, no crit) unexpected value"
    
    # after resetting buffs
    if "Divine Purpose" in paladin.active_auras:
        del paladin.active_auras["Divine Purpose"]
    paladin.holy_power = 3
    paladin.global_cooldown = 0
    _, _, heal_amount, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(40587 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Word of Glory (Unending Light - 9 stacks, no crit) unexpected value"
    
def test_light_of_dawn():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(9760 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Light of Dawn (no talents, no crit) unexpected value"
    
def test_light_of_dawn_divine_purpose():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Purpose": 1}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(DivinePurpose(), 0)
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(9760 * 1.15 / 100) * 100
    assert round(heal_amount / 100) * 100 == expected_heal_amount, "Light of Dawn (Divine Purpose, no crit) unexpected value"
    
def test_light_of_dawn_blessing_of_dawn():
    # no talents, no crit
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Of Dusk and Dawn": 1}, {"Light of Dawn": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    target = [targets[0]]
    paladin.crit = -100
    paladin.holy_power = 3
    paladin.apply_buff_to_self(BlessingOfDawn(), 0)
    _, _, heal_amount, _ = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = round(9760 * 1.3 / 10) * 10
    assert round(heal_amount / 10) * 10 == expected_heal_amount, "Light of Dawn (Of Dusk and Dawn, no crit) unexpected value"
    
def test_light_of_dawn_empyrean_legacy():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Empyrean Legacy": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
       
    target = [targets[0]]
    paladin.crit = -100
    _, _, _, _, _ = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    paladin.global_cooldown = 0
    paladin.holy_power = 3
    _, _, _, _, _, light_of_dawn_healing = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 61000
    assert expected_heal_amount - 1000 <= round(light_of_dawn_healing / 10) * 10 <= expected_heal_amount + 1000, "Light of Dawn (Empyrean Legacy) unexpected value"
    
def test_glimmer_illumination():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_glimmer_healing = round(19227 / 10) * 10
    assert round(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (no talents, no crit) unexpected value"
    
def test_glimmer_illumination_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1, "Glorious Dawn": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        glimmer_count = min(i + 1, 8)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
        expected_glimmer_healing = math.ceil(19227 * 1.1 * glimmer_bonus / 100) * 100
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (no talents, no crit) unexpected value"
        
def test_glimmer_illumination_rising_sunlight():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1, "Rising Sunlight": 1})
    
    rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_glimmer_healing = round(19227 / 10) * 10
    assert round(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (Rising Sunlight, no crit) unexpected value"
    
def test_glimmer_illumination_rising_sunlight_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1, "Glorious Dawn": 1, "Rising Sunlight": 1})
        
        rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
        
        glimmer_count = min(i + 1, 8)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
        expected_glimmer_healing = math.ceil(19227 * 1.1 * glimmer_bonus / 100) * 100
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Rising Sunlight, no crit) unexpected value"
        
def test_glimmer_illumination_divine_resonance():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Resonance": 1}, {"Glimmer of Light": 1, "Illumination": 1})
    
    divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_glimmer_healing = 0
    assert round(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (Divine Resonance, no crit) unexpected value"
    
def test_glimmer_illumination_divine_resonance_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {"Divine Resonance": 1}, {"Glimmer of Light": 1, "Illumination": 1, "Glorious Dawn": 1})
        
        divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
        
        glimmer_count = min(i + 1, 8)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
        expected_glimmer_healing = 0
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Divine Resonance, no crit) unexpected value"
        
def test_glimmer_illumination_daybreak():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1, "Daybreak": 1})
    
    daybreak = paladin.abilities["Daybreak"]
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing = daybreak.cast_healing_spell(paladin, target, 0, False, glimmer_targets)
    
    expected_glimmer_healing = math.ceil(19227 * 2 / 10) * 10
    assert math.ceil(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (Daybreak, no crit) unexpected value"
    
def test_glimmer_illumination_daybreak_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1, "Glorious Dawn": 1, "Daybreak": 1})
        
        daybreak = paladin.abilities["Daybreak"]
        
        glimmer_count = min(i + 1, 8)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing = daybreak.cast_healing_spell(paladin, target, 0, False, glimmer_targets)
    
        expected_glimmer_healing = round(19227 * 2 * 1.1 * glimmer_bonus / 100) * 100
        assert round(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Daybreak, no crit) unexpected value"
        
def test_glistening_radiance_word_of_glory():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1, "Glistening Radiance": 1})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    
    target = [targets[0]]
    glimmer_healing = 0
    while glimmer_healing == 0:
        paladin.holy_power = 3
        _, _, _, glimmer_healing, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0        
    
    expected_glimmer_healing = math.ceil(19227 / 10) * 10
    assert math.ceil(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (Glistening Radiance - Word of Glory, no crit) unexpected value"
    
def test_glistening_radiance_glorious_dawn_word_of_glory():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Glimmer of Light": 1, "Illumination": 1, "Glorious Dawn": 1, "Glistening Radiance": 1})
        
        word_of_glory = paladin.abilities["Word of Glory"]
        
        glimmer_count = min(i + 1, 8)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        
        target = [targets[0]]
        glimmer_healing = 0
        while glimmer_healing == 0:
            paladin.holy_power = 3
            _, _, _, glimmer_healing, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
            paladin.global_cooldown = 0    
    
        expected_glimmer_healing = math.ceil(19227 * 1.1 * glimmer_bonus / 100) * 100
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Glistening Radiance - Word of Glory, no crit) unexpected value"
        
def test_glistening_radiance_light_of_dawn():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Light of Dawn": 1, "Glimmer of Light": 1, "Illumination": 1, "Glistening Radiance": 1})
    
    light_of_dawn = paladin.abilities["Light of Dawn"]
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    
    target = [targets[0]]
    glimmer_healing = 0
    while glimmer_healing == 0:
        paladin.holy_power = 3
        _, _, _, glimmer_healing = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0        
    
    expected_glimmer_healing = math.ceil(19227 / 10) * 10
    assert math.ceil(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (Glistening Radiance - Light of Dawn, no crit) unexpected value"
    
def test_glistening_radiance_glorious_dawn_light_of_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Light of Dawn": 1, "Glimmer of Light": 1, "Illumination": 1, "Glorious Dawn": 1, "Glistening Radiance": 1})
        
        light_of_dawn = paladin.abilities["Light of Dawn"]
        
        glimmer_count = min(i + 1, 8)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        
        target = [targets[0]]
        glimmer_healing = 0
        while glimmer_healing == 0:
            paladin.holy_power = 3
            _, _, _, glimmer_healing = light_of_dawn.cast_healing_spell(paladin, target, 0, True)
            paladin.global_cooldown = 0    
    
        expected_glimmer_healing = math.ceil(19227 * 1.1 * glimmer_bonus / 100) * 100
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Glistening Radiance -Light of Dawny, no crit) unexpected value"

def test_glimmer_blessed_focus():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Glimmer of Light": 1, "Blessed Focus": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_glimmer_healing = round(19227 * 1.4 / 10) * 10
    assert round(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (no talents, no crit) unexpected value"
    
def test_glimmer_blessed_focus_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Glimmer of Light": 1, "Blessed Focus": 1, "Glorious Dawn": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        glimmer_count = min(i + 1, 3)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
        expected_glimmer_healing = math.ceil(19227 * 1.1 * glimmer_bonus * 1.4 / 100) * 100
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (no talents, no crit) unexpected value"
        
def test_glimmer_blessed_focus_rising_sunlight():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Glimmer of Light": 1, "Blessed Focus": 1, "Rising Sunlight": 1})
    
    rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_glimmer_healing = round(19227 * 1.4 / 10) * 10
    assert expected_glimmer_healing - 100 <= round(glimmer_healing / 10) * 10 <= expected_glimmer_healing + 100, "Glimmer of Light (Rising Sunlight, no crit) unexpected value"
    
def test_glimmer_blessed_focus_rising_sunlight_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Glimmer of Light": 1, "Blessed Focus": 1, "Glorious Dawn": 1, "Rising Sunlight": 1})
        
        rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
        
        glimmer_count = min(i + 1, 3)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing, _ = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
        expected_glimmer_healing = math.ceil(19227 * 1.1 * glimmer_bonus * 1.4 / 100) * 100
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Rising Sunlight, no crit) unexpected value"
        
def test_glimmer_blessed_focus_divine_resonance():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Divine Resonance": 1}, {"Glimmer of Light": 1, "Blessed Focus": 1})
    
    divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_glimmer_healing = 0
    assert round(glimmer_healing / 10) * 10 == expected_glimmer_healing, "Glimmer of Light (Divine Resonance, no crit) unexpected value"
    
def test_glimmer_blessed_focus_divine_resonance_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {"Divine Resonance": 1}, {"Glimmer of Light": 1, "Blessed Focus": 1, "Glorious Dawn": 1})
        
        divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
        
        glimmer_count = min(i + 1, 3)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing, _ = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
        expected_glimmer_healing = 0 * 1.4
        assert math.ceil(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Divine Resonance, no crit) unexpected value"
        
def test_glimmer_blessed_focus_daybreak():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Glimmer of Light": 1, "Blessed Focus": 1, "Daybreak": 1})
    
    daybreak = paladin.abilities["Daybreak"]
    
    paladin.crit = -10
    
    chosen_targets = random.sample(paladin.potential_healing_targets, 1)
    for target in chosen_targets:
        target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
    glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
    
    target = [targets[0]]
    _, _, _, glimmer_healing = daybreak.cast_healing_spell(paladin, target, 0, False, glimmer_targets)
    
    expected_glimmer_healing = math.ceil(19227 * 2 * 1.4 / 10) * 10
    assert expected_glimmer_healing - 100 <= math.ceil(glimmer_healing / 10) * 10 <= expected_glimmer_healing + 100, "Glimmer of Light (Daybreak, no crit) unexpected value"
    
def test_glimmer_blessed_focus_daybreak_glorious_dawn():    
    for i in range(8):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {"Glimmer of Light": 1, "Blessed Focus": 1, "Glorious Dawn": 1, "Daybreak": 1})
        
        daybreak = paladin.abilities["Daybreak"]
        
        glimmer_count = min(i + 1, 3)
        if glimmer_count == 1:
            glimmer_bonus = 1
        else:
            glimmer_bonus = 1 + glimmer_count * 0.04
        
        paladin.crit = -10
        
        chosen_targets = random.sample(paladin.potential_healing_targets, glimmer_count)
        for target in chosen_targets:
            target.apply_buff_to_target(GlimmerOfLightBuff(), 0, caster=paladin)
        glimmer_targets = [glimmer_target for glimmer_target in paladin.potential_healing_targets if "Glimmer of Light" in glimmer_target.target_active_buffs]
        
        target = [targets[0]]
        _, _, _, glimmer_healing = daybreak.cast_healing_spell(paladin, target, 0, False, glimmer_targets)
    
        expected_glimmer_healing = round(19227 * 2 * 1.1 * glimmer_bonus * 1.4 / 100) * 100
        assert round(glimmer_healing / 100) * 100 == expected_glimmer_healing, "Glimmer of Light (Glorious Dawn, Daybreak, no crit) unexpected value"     
        
def test_afterimage():
    # 1 glimmer
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Afterimage": 1}, {})
    
    word_of_glory = paladin.abilities["Word of Glory"]
    
    paladin.crit = -10
    
    target = [targets[0]]
    word_of_glory_healing = 0
    afterimage_healing = 0
    while paladin.afterimage_counter < 17:
        paladin.holy_power = 3
        _, _, _, _, _, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
        paladin.global_cooldown = 0
        
    if paladin.afterimage_counter >= 17:
        
        paladin.holy_power = 3
        _, _, word_of_glory_healing, _, afterimage_healing, _ = word_of_glory.cast_healing_spell(paladin, target, 0, True)
    
    expected_afterimage_healing = math.ceil(40587 * 0.3 / 10) * 10
    assert math.ceil(afterimage_healing / 10) * 10 == expected_afterimage_healing, "Afterimage unexpected value"
    
def test_avenging_wrath_healing_increase():
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -100
        paladin.apply_buff_to_self(AvengingWrathBuff(paladin), 0)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(17980 * 1.15 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (Avenging Wrath, no crit) unexpected value"
        
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -100
        paladin.apply_buff_to_self(AvengingWrathAwakening(), 0)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(17980 * 1.15 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (Avenging Wrath (Awakening), no crit) unexpected value"
        
def test_avenging_wrath_crit_chance_holy_shock():
    iterations = 10000
    crits = 0
    
    for _ in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {"Avenging Wrath": 1}, {"Avenging Wrath: Might": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        avenging_wrath = paladin.abilities["Avenging Wrath"]
        
        target = [targets[0]]
        avenging_wrath.cast_healing_spell(paladin, target, 0, False)
        _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        if heal_crit:
            crits += 1
            
    holy_shock_bonus_crit = 0.1
    paladin.remove_or_decrement_buff_on_self(paladin.active_auras["Avenging Wrath"], 0)
            
    expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit + 0.15
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
    iterations = 10000
    crits = 0
    
    for _ in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {"Avenging Wrath": 1}, {"Avenging Wrath: Might": 1})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        target = [targets[0]]
        paladin.apply_buff_to_self(AvengingWrathAwakening(), 0)
        _, heal_crit, _, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        if heal_crit:
            crits += 1
            
    holy_shock_bonus_crit = 0.1
    paladin.remove_or_decrement_buff_on_self(paladin.active_auras["Avenging Wrath (Awakening)"], 0)
            
    expected_crit_rate = paladin.crit / 100 + holy_shock_bonus_crit + 0.15
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
def test_avenging_wrath_crit_chance_holy_light():
    iterations = 10000
    crits = 0
    
    for _ in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {"Avenging Wrath": 1}, {"Avenging Wrath: Might": 1})
        
        holy_light = paladin.abilities["Holy Light"]
        avenging_wrath = paladin.abilities["Avenging Wrath"]
        
        target = [targets[0]]
        avenging_wrath.cast_healing_spell(paladin, target, 0, False)
        _, heal_crit, _, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        if heal_crit:
            crits += 1
            
    paladin.remove_or_decrement_buff_on_self(paladin.active_auras["Avenging Wrath"], 0)
            
    expected_crit_rate = paladin.crit / 100 + 0.15
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (no talents)"
    
    iterations = 10000
    crits = 0
    
    for _ in range(iterations):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {"Avenging Wrath": 1}, {"Avenging Wrath: Might": 1})
        
        holy_light = paladin.abilities["Holy Light"]
        
        target = [targets[0]]
        paladin.apply_buff_to_self(AvengingWrathAwakening(), 0)
        _, heal_crit, _, _, _ = holy_light.cast_healing_spell(paladin, target, 0, True)
        if heal_crit:
            crits += 1
            
    paladin.remove_or_decrement_buff_on_self(paladin.active_auras["Avenging Wrath (Awakening)"], 0)
            
    expected_crit_rate = paladin.crit / 100 + 0.15
    observed_crit_rate = crits / iterations
    
    print(f"Expected crit rate: {expected_crit_rate}")
    print(f"Observed crit rate: {observed_crit_rate}")
    
    tolerance = 0.02
    assert abs(observed_crit_rate - expected_crit_rate) <= tolerance, "Observed crit rate does not match expected crit rate (Awakening)"
        
def test_blessing_of_spring():
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        holy_shock = paladin.abilities["Holy Shock"]
        
        paladin.crit = -100
        paladin.apply_buff_to_self(BlessingOfSpring(), 0)
        
        target = [targets[0]]
        _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
        
        expected_heal_amount = round(17980 * 1.15 / 10) * 10
        assert round(heal_amount / 10) * 10 == expected_heal_amount, "Holy Shock (Blessing of Spring, no crit) unexpected value"
        
def test_touch_of_light():
    for _ in range(100):
        paladin = initialise_paladin()
        targets, glimmer_targets = set_up_paladin(paladin)
        
        reset_talents(paladin)
        update_talents(paladin, {}, {})
        
        touch_of_light = TouchOfLight(paladin)
        
        paladin.crit = -100
        
        target = [targets[0]]
        _, _, heal_amount = touch_of_light.cast_healing_spell(paladin, target, 0, True, exclude_mastery=True)
        
        expected_heal_amount = round(26202 / 10) * 10
        assert expected_heal_amount - 100 <= round(heal_amount / 10) * 10 <= expected_heal_amount + 100, "Touch of Light unexpected value"
        
def test_judgment_of_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Judgment of Light": 1}, {})
    
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
    
    paladin.crit = -100
    
    target = [targets[0]]
    _, _, _, judgment_of_light_healing, _ = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    
    expected_heal_amount = round(2050 * 5 / 10) * 10
    assert expected_heal_amount - 100 <= round(judgment_of_light_healing / 10) * 10 <= expected_heal_amount + 100, "Judgment of Light unexpected value"
    
def test_greater_judgment():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Greater Judgment": 1}, {})
    
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
    
    paladin.crit = -100
    
    target = [targets[0]]
    _, _, _, _, greater_judgment_healing = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    
    expected_heal_amount = round(21365 / 10) * 10
    assert expected_heal_amount - 100 <= round(greater_judgment_healing / 10) * 10 <= expected_heal_amount + 100, "Greater Judgment unexpected value"
    
def test_greater_judgment_infusion_of_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Greater Judgment": 1}, {})
    
    holy_shock = paladin.abilities["Holy Shock"]
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
    
    set_crit_to_max(paladin)
    target = [targets[0]]
    _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.crit = -100
    _, _, _, _, greater_judgment_healing = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    
    expected_heal_amount = round(21365 * 2 / 10) * 10
    assert expected_heal_amount - 100 <= round(greater_judgment_healing / 10) * 10 <= expected_heal_amount + 100, "Greater Judgment (Infusion of Light) unexpected value"
    
def test_greater_judgment_infusion_of_light_inflorescence_of_the_sunwell():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Greater Judgment": 1}, {"Inflorescence of the Sunwell": 1})
    
    holy_shock = paladin.abilities["Holy Shock"]
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
       
    set_crit_to_max(paladin)
    target = [targets[0]]
    _, _, heal_amount, _, _ = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    paladin.global_cooldown = 0
    paladin.crit = -100
    _, _, _, _, greater_judgment_healing = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    
    expected_heal_amount = round(21365 * 2.5 / 10) * 10
    assert expected_heal_amount - 100 <= round(greater_judgment_healing / 10) * 10 <= expected_heal_amount + 100, "Greater Judgment (Infusion of Light, Inflorescence of the Sunwell) unexpected value"
    
def test_greater_judgment_avenging_wrath():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Avenging Wrath": 1, "Greater Judgment": 1}, {})
    
    judgment = paladin.abilities["Judgment"]
    enemy_target = EnemyTarget("enemyTarget1")
    
    paladin.crit = -100
    paladin.apply_buff_to_self(AvengingWrathBuff(paladin), 0)
    
    target = [targets[0]]
    _, _, _, _, greater_judgment_healing = judgment.cast_damage_spell(paladin, [enemy_target], 0, targets)
    
    expected_heal_amount = round(21365 * 1.15 / 10) * 10
    assert expected_heal_amount - 100 <= round(greater_judgment_healing / 10) * 10 <= expected_heal_amount + 100, "Greater Judgment unexpected value"
    
def test_crusaders_reprieve():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {"Crusader's Reprieve": 1}, {})
    
    crusader_strike = paladin.abilities["Crusader Strike"]
    enemy_target = EnemyTarget("enemyTarget1")
       
    set_crit_to_max(paladin)
    target = [targets[0]]
    _, _, _, crusaders_reprieve_healing = crusader_strike.cast_damage_spell(paladin, [enemy_target], 0, targets)
    
    # TODO fix when stamina calculation is fixed
    expected_heal_amount = paladin.max_health * 0.02
    assert expected_heal_amount - 100 <= round(crusaders_reprieve_healing / 10) * 10 <= expected_heal_amount + 100, "Crusader's Reprieve unexpected value"
    
def test_barrier_of_faith_initial_absorb():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
       
    paladin.crit = -100
    target = [targets[0]]
    _, _, barrier_of_faith_healing = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 58050
    assert expected_heal_amount - 100 <= round(barrier_of_faith_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light Initial Absorb unexpected value"
    
def test_barrier_of_faith_holy_shock():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
    holy_shock = paladin.abilities["Holy Shock"]
    
    # regular holy shock
    paladin.crit = -100
    target = [targets[0]]
    _, _, _ = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 0.25
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Holy Shock) unexpected value"
    
    # divine resonance
    divine_resonance_holy_shock = DivineResonanceHolyShock(paladin)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = divine_resonance_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 0.25
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Divine Resonance Holy Shock) unexpected value"
    
    # divine toll
    divine_toll_holy_shock = DivineTollHolyShock(paladin)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = divine_toll_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 0.25
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Divine Toll Holy Shock) unexpected value"
    
    # rising sunlight
    rising_sunlight_holy_shock = RisingSunlightHolyShock(paladin)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_shock_healing = rising_sunlight_holy_shock.cast_healing_spell(paladin, target, 0, True, glimmer_targets)
    
    expected_heal_amount = 17980 * 0.25
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_shock_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Rising Sunlight Holy Shock) unexpected value"
    
def test_barrier_of_faith_holy_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
    holy_light = paladin.abilities["Holy Light"]
    
    paladin.crit = -100
    target = [targets[0]]
    _, _, _ = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, _, barrier_of_faith_holy_light_healing = holy_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 59692 * 0.25
    assert expected_heal_amount - 100 <= round(barrier_of_faith_holy_light_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Holy Light) unexpected value"
    
def test_barrier_of_faith_flash_of_light():
    paladin = initialise_paladin()
    targets, glimmer_targets = set_up_paladin(paladin)
    
    reset_talents(paladin)
    update_talents(paladin, {}, {"Barrier of Faith": 1})
    
    barrier_of_faith = paladin.abilities["Barrier of Faith"]
    flash_of_light = paladin.abilities["Flash of Light"]
    
    paladin.crit = -100
    target = [targets[0]]
    _, _, _ = barrier_of_faith.cast_healing_spell(paladin, target, 0, True)
    paladin.global_cooldown = 0
    _, _, _, barrier_of_faith_flash_of_light_healing = flash_of_light.cast_healing_spell(paladin, target, 0, True)
    
    expected_heal_amount = 46210 * 0.25
    assert expected_heal_amount - 100 <= round(barrier_of_faith_flash_of_light_healing / 10) * 10 <= expected_heal_amount + 100, "Barrier of Light (Flash of Light) unexpected value"