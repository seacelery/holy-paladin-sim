import unittest
import re

from classes.simulation import Simulation
from classes.paladin import Paladin
from classes.target import Target, BeaconOfLight
from classes.spells import Wait
from classes.spells_auras import DivineFavorSpell
from classes.spells_healing import HolyShock, WordOfGlory, LightOfDawn, FlashOfLight, HolyLight, DivineToll, Daybreak, LightsHammerSpell
from classes.spells_damage import Judgment, CrusaderStrike
from classes.auras_buffs import HolyReverberation
from talents.base_talent_dictionaries import base_active_class_talents, base_active_spec_talents


stats_data = {
    "health": 407620,
    "power": 262500,
    "intellect": {
        "effective": 9476
    },
    "spell_haste": {
        "rating": 3511,
        "rating_bonus": 20.653498,
        "value": 20.653496
    },
    "spell_crit": {
        "rating": 1473,
        "rating_bonus": 8.183554,
        "value": 13.183554
    },
    "mastery": {
        "rating": 972,
        "rating_bonus": 8.100218,
        "value": 20.100218
    },
    "versatility": 3653.0,
    "versatility_healing_done_bonus": 17.819992,
    "lifesteal": {
        "rating": 1188,
        "rating_bonus": 8.027243,
        "value": 8.027243
    },
    "stamina": {
        "effective": 20381
    }
}

# class TestHolyShockInteractions(unittest.TestCase):
#     def setUp(self):
#         # return
#         self.targets = targets = [Target(f"target{i + 1}") for i in range(18)] + [BeaconOfLight(f"beaconTarget{i + 1}") for i in range(2)]
#         self.paladin = Paladin("Test Paladin", stats_data, potential_healing_targets=targets)
#         self.beacon_targets = [target for target in targets if isinstance(target, BeaconOfLight)]
#         self.paladin.set_beacon_targets(self.beacon_targets)
        
#         self.simulation = Simulation(self.paladin, targets, 40)
   
#         self.stats = self.paladin.parse_stats(stats_data)
#         self.haste = 22.98
#         self.crit = 20
#         self.mastery = 24.79
#         self.versatility = 21.49
#         self.spell_power = 9340
        
#         self.haste_multiplier = (self.haste / 100) + 1
#         self.crit_multiplier = (self.crit / 100) + 1
#         self.mastery_multiplier = (self.mastery / 100) + 1
#         self.versatility_multiplier = (self.versatility / 100) + 1
    
#     def test_infusion_of_light_proc(self):
#         # return
#         self.simulation.priority_list = [
#             (self.paladin.abilities["Holy Shock"], lambda:  self.simulation.elapsed_time <= 1),
#         ]  
        
#         # set crit to 0 to make it easier
#         self.paladin.crit = 100
        
#         self.simulation.simulate()
#         results = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
#         holy_shock_crit = re.findall(r'(\d+\.\d+): Holy Shock crit', results)
#         infusion_of_light_applied = re.findall(r'(\d+\.\d+): Infusion of Light \((\d+)\) applied to', results)
        
#         self.assertEqual(holy_shock_crit[0], infusion_of_light_applied[0][0])
       
#     def test_holy_reverberation_haste_change(self):
#         # return
#         # requires single target
#         # uses daybreak without a glimmer active to check haste
        
#         self.simulation.priority_list = [
#             (self.paladin.abilities["Holy Shock"], lambda:  self.simulation.elapsed_time >= 15 and self.simulation.elapsed_time <= 16),
#             (self.paladin.abilities["Holy Shock"], lambda:  self.simulation.elapsed_time <= 1),
#             (self.paladin.abilities["Daybreak"], lambda: self.simulation.elapsed_time >= 16.22),
#         ]  
        
#         # set crit to 0 to make it easier
#         self.paladin.crit = 0
        
#         self.simulation.simulate()
#         results = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
#         holy_reverberation_applied = re.findall(r'(\d+\.\d+): Holy Reverberation \((\d+)\) applied to (target\d+)', results)
#         holy_reverberation_first_stack_applied_time = float(holy_reverberation_applied[0][0])
        
#         holy_reverberation_second_stack_applied_time = float(holy_reverberation_applied[1][0])
        
#         holy_reverberation_removed = re.findall(r'(\d+\.\d+): Holy Reverberation removed from (target\d+)', results)
#         holy_reverberation_removed_time = float(holy_reverberation_removed[0][0])
        
#         first_light_applied = re.findall(r'(\d+\.\d+): First Light applied', results)
#         first_light_applied_time = float(first_light_applied[0])
        
#         first_light_removed = re.findall(r'(\d+\.\d+): First Light removed', results)
#         first_light_removed_time = float(first_light_removed[0])
        
#         tick_healing = re.findall(r'(\d+\.\d+): Holy Reverberation healed target\d+ for (\d+)', results)
        
#         tick_interval = HolyReverberation(self.paladin).base_tick_interval / self.paladin.haste_multiplier
#         hasted_tick_interval = tick_interval * self.paladin.haste_multiplier / (self.paladin.haste_multiplier * 1.25)
        
#         total_healing = HolyReverberation(self.paladin).SPELL_POWER_COEFFICIENT * self.spell_power * self.mastery_multiplier * self.versatility_multiplier
#         calculated_regular_tick_healing = int(total_healing / 8)
        
#         second_to_last_tick_time = float(tick_healing[-2][0])
#         calculated_partial_tick_healing = int(calculated_regular_tick_healing * ((holy_reverberation_removed_time - second_to_last_tick_time) / tick_interval))
        
#         for tick_time, tick_value in tick_healing:
#             tick_time = float(tick_time)
#             tick_value = int(tick_value)
#             if tick_time < first_light_applied_time:
#                 self.assertEqual(calculated_regular_tick_healing, tick_value)
            
#             # make sure ticks are hasted properly
#             elif tick_time > first_light_applied_time and tick_time < first_light_removed_time:
#                 tolerance = 0.015
#                 tick_difference = round(tick_time - previous_tick_time, 2)
#                 if tick_time > first_light_applied_time and tick_time < first_light_removed_time:
#                     self.assertEqual(round((calculated_regular_tick_healing * 2) / 10) * 10, round(tick_value / 10) * 10)
#                     if tick_difference >= tick_interval:
#                         pass
#                     else:
#                         is_within_tolerance = abs(tick_difference - hasted_tick_interval) <= tolerance
#                         self.assertTrue(is_within_tolerance, f"{tick_difference} is not within the acceptable range of {hasted_tick_interval} ± {tolerance}")
            
#             # make sure partial tick is correct            
#             elif tick_time > second_to_last_tick_time:
#                 is_acceptable_partial_tick = calculated_partial_tick_healing in range(tick_value - 10, tick_value + 11)
#                 self.assertTrue(is_acceptable_partial_tick, f"{calculated_partial_tick_healing} is not within the acceptable range ({tick_value - 10}, {tick_value + 10})")
                
#             previous_tick_time = tick_time

#     def test_holy_reverberation_glimmer_expires(self):
#         # return
#         self.simulation.priority_list = [
#             (self.paladin.abilities["Holy Shock"], lambda: self.simulation.elapsed_time <= 1),
#         ]  
        
#         self.simulation.holy_shock_target_selection == "Single"
        
#         self.simulation.simulate()
#         results = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
#         glimmer_expires = r'30.00: Glimmer of Light removed from (beacon_)?target\d+'
#         holy_reverberation_applied = r'30.00: Holy Reverberation \(1\) applied to (beacon_)?target\d+: 8s duration'
#         holy_reverberation_expires = r'38.00: Holy Reverberation removed from (beacon_)?target\d+'
#         holy_reverberation_tick_count = len(re.findall(r'Holy Reverberation (crit )?healed', results))
        
#         self.assertIsNotNone(re.search(glimmer_expires, results))
#         self.assertIsNotNone(re.search(holy_reverberation_applied, results))
#         self.assertIsNotNone(re.search(holy_reverberation_expires, results))
#         self.assertEqual(holy_reverberation_tick_count, 10)
        
#     def test_holy_reverberation_glimmer_reapplied_at_cap(self):
#         # return
#         # requires multi target

#         self.simulation.priority_list = [
#             (self.paladin.abilities["Holy Shock"], lambda: self.simulation.elapsed_time <= 20),
#             (self.paladin.abilities["Divine Toll"], lambda: True),
#         ]  
        
#         self.simulation.simulate()
#         results = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
#         first_glimmer_target = re.findall(r'Holy Shock (?:\(Divine Toll\) )?(?:crit )?healed (target\d+)', results)
#         print(first_glimmer_target)
#         glimmer_removed_from = re.findall(r'Glimmer of Light removed from (target\d+)', results)
#         print(glimmer_removed_from)
#         holy_reverberation_applied_to = re.findall(r'Holy Reverberation \(1\) applied to (target\d+)', results)
#         print(holy_reverberation_applied_to)
        
#         self.assertEqual(first_glimmer_target[0], glimmer_removed_from[0], holy_reverberation_applied_to[0])
    
#     def test_holy_reverberation_partial_tick(self):
#         # return
#         # requires single target
#         self.simulation.priority_list = [
#             (self.paladin.abilities["Holy Shock"], lambda: 15 <= self.simulation.elapsed_time <= 20),
#         ]  
        
#         # set crit to 0 to make it easier
#         self.paladin.crit = 0
        
#         self.simulation.simulate()
#         results = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
#         holy_reverberation_applied = re.findall(r'(\d+\.\d+): Holy Reverberation \(1\) applied to (target\d+)', results)
#         holy_reverberation_applied_time = float(holy_reverberation_applied[0][0])
        
#         holy_reverberation_removed = re.findall(r'(\d+\.\d+): Holy Reverberation removed from (target\d+)', results)
#         holy_reverberation_removed_time = float(holy_reverberation_removed[0][0])
        
#         tick_healing = re.findall(r'(\d+\.\d+): Holy Reverberation healed target\d+ for (\d+)', results)
        
#         tick_interval = HolyReverberation(self.paladin).base_tick_interval / self.paladin.haste_multiplier
        
#         # confirm that it's ticking at the correct intervals
#         previous_tick_time = 16.22
#         count = 0
#         for tick_time, value in tick_healing:
#             if count == 9:
#                 break
            
#             interval = round(float(tick_time) - previous_tick_time, 2)
#             is_acceptable_interval = interval in [round(tick_interval, 2), round(tick_interval + 0.01, 2)]
#             self.assertTrue(is_acceptable_interval, f"Interval {interval} is not within the acceptable range ({round(tick_interval, 2)}, {round(tick_interval + 0.01, 2)})")

#             previous_tick_time = float(tick_time)
#             count += 1
        
#         # check 8 seconds duration
#         self.assertEqual(holy_reverberation_removed_time - holy_reverberation_applied_time, 8)
        
#         # check partial tick is behaving properly
#         regular_tick_healing = int(tick_healing[1][1])
#         partial_tick_healing = int(tick_healing[-1][1])
#         second_to_last_tick_time = float(tick_healing[-2][0])
        
#         calculated_partial_tick_healing = int(regular_tick_healing * ((holy_reverberation_removed_time - second_to_last_tick_time) / tick_interval))
        
#         is_acceptable_partial_tick = calculated_partial_tick_healing in [partial_tick_healing - 10, partial_tick_healing + 10]
#         self.assertTrue(is_acceptable_partial_tick, f"{calculated_partial_tick_healing} is not within the acceptable range ({partial_tick_healing - 15}, {partial_tick_healing + 15})")
        
#         # self.assertEqual()
        
#     def test_holy_reverberation_stacks(self):
#         # return
#         # requires single target
        
#         self.simulation.priority_list = [
#             (self.paladin.abilities["Holy Shock"], lambda: self.simulation.elapsed_time <= 1 or (15 <= self.simulation.elapsed_time <= 23)),
#         ]  
        
#         self.simulation.simulate()
#         results = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
#         # make sure it's using holy shock on the same target for holy reverberation to proc
#         holy_shocks_same_target = re.findall(r'Holy Shock (?:crit )?healed (target\d+)', results)
        
#         first_holy_shock = holy_shocks_same_target[0]
#         for holy_shock in holy_shocks_same_target[1:]:
#             self.assertEqual(first_holy_shock, holy_shock)
            
#         holy_reverberation_first_stack_applied = re.findall(r'(\d+\.\d+): Holy Reverberation \(1\) applied to (target\d+)', results)
#         first_stack_applied_time = float(holy_reverberation_first_stack_applied[0][0])
        
#         holy_reverberation_second_stack_applied = re.findall(r'(\d+\.\d+): Holy Reverberation \(2\) applied to (target\d+)', results)
#         second_stack_applied_time = float(holy_reverberation_second_stack_applied[0][0])
        
#         holy_reverberation_first_stack_removed = re.findall(fr'(\d+\.\d+): Holy Reverberation \(1\) on (target\d+): {round(second_stack_applied_time - first_stack_applied_time, 2)}s remaining', results)
#         first_stack_removed_time = float(holy_reverberation_first_stack_removed[0][0])
        
#         holy_reverberation_second_stack_removed = re.findall(r'(\d+\.\d+): Holy Reverberation removed from (target\d+)', results)
#         second_stack_removed_time = float(holy_reverberation_second_stack_removed[0][0])
        
#         holy_reverberation_tick_count = len(re.findall(r'Holy Reverberation (crit )?healed', results))
        
#         # ensure no desync and buffs are 8 seconds long
#         self.assertEqual(second_stack_removed_time - first_stack_removed_time, second_stack_applied_time - first_stack_applied_time)
#         self.assertEqual(first_stack_removed_time - first_stack_applied_time, 8)
#         self.assertEqual(second_stack_removed_time - second_stack_applied_time, 8)
#         self.assertEqual(holy_reverberation_tick_count, 12)
    
class TestPaladinTalents(unittest.TestCase):     
    def setUp(self):
        self.targets = [Target(f"target{i + 1}") for i in range(18)] + [BeaconOfLight(f"beaconTarget{i + 1}") for i in range(2)]
        self.paladin = Paladin("Test Paladin", stats_data=stats_data, potential_healing_targets=self.targets)
        self.beacon_targets = [target for target in self.targets if isinstance(target, BeaconOfLight)]
        self.paladin.set_beacon_targets(self.beacon_targets)
        self.paladin.class_talents = base_active_class_talents
        self.paladin.spec_talents = base_active_spec_talents
        
        self.paladin.abilities = {
                            "Wait": Wait(),
                            "Flash of Light": FlashOfLight(self.paladin),
                            "Holy Light": HolyLight(self.paladin),
                            "Crusader Strike": CrusaderStrike(self.paladin),
                            "Judgment": Judgment(self.paladin),
                            "Word of Glory": WordOfGlory(self.paladin),
        }   
        
        # for row, row_data in self.paladin.class_talents.items():
        #     for talent in row_data:
        #         self.paladin.class_talents[row][talent]["ranks"]["current rank"] = 0
                
        # for row, row_data in self.paladin.spec_talents.items():
        #     for talent in row_data:
        #         self.paladin.spec_talents[row][talent]["ranks"]["current rank"] = 0
                

        self.paladin.class_talents["row3"]["Greater Judgment"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row5"]["Justification"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row5"]["Avenging Wrath"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row7"]["Afterimage"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row7"]["Crusader's Reprieve"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row8"]["Judgment of Light"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row8"]["Divine Purpose"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row8"]["Touch of Light"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row9"]["Of Dusk and Dawn"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row10"]["Divine Resonance"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row10"]["Seal of Order"]["ranks"]["current rank"] = 0
        self.paladin.class_talents["row10"]["Quickened Invocation"]["ranks"]["current rank"] = 0
        
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row3"]["Light's Conviction"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row4"]["Resplendent Light"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row4"]["Awestruck"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row5"]["Divine Favor"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row5"]["Glistening Radiance"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row5"]["Imbued Infusions"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row6"]["Light's Hammer"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row6"]["Illumination"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row7"]["Tower of Radiance"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row7"]["Divine Revelations"]["ranks"]["current rank"] = 0   
        self.paladin.spec_talents["row7"]["Divine Glimpse"]["ranks"]["current rank"] = 0 
        self.paladin.spec_talents["row8"]["Avenging Wrath: Might"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row8"]["Reclamation"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row9"]["Tyr's Deliverance"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row9"]["Blessing of Summer"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row10"]["Rising Sunlight"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row10"]["Glorious Dawn"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row10"]["Awakening"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row10"]["Inflorescence of the Sunwell"]["ranks"]["current rank"] = 0
        self.paladin.spec_talents["row10"]["Boundless Salvation"]["ranks"]["current rank"] = 0
        
        self.holy_shock_cooldown_overflow = 0
        self.infused_holy_light_count = 0
        self.divine_resonance_timer = 0
        self.divine_toll_holy_shock_count = 0
        self.delayed_casts = []
        self.rising_sunlight_timer = 0
        self.tyrs_deliverance_extended_by = 0
        self.blessing_of_dawn_counter = 0
        self.afterimage_counter = 0
        
        self.paladin.mana_regen_per_second = 2000
          
        self.paladin.load_abilities_based_on_talents()
        
        self.paladin.stats = self.paladin.parse_stats(stats_data)
        self.paladin.haste = 22.98
        self.paladin.crit = 20
        self.paladin.mastery = 24.79
        self.paladin.versatility = 21.49
        self.paladin.spell_power = 9340
        self.paladin.max_health = 425000
        
        self.paladin.haste_multiplier = (self.paladin.haste / 100) + 1
        self.paladin.crit_multiplier = (self.paladin.crit / 100) + 1
        self.paladin.mastery_multiplier = (self.paladin.mastery / 100) + 1
        self.paladin.versatility_multiplier = (self.paladin.versatility / 100) + 1
        
    def test_judgment_talents(self):
        # return
        self.simulation = Simulation(self.paladin, self.targets, 40)
        self.simulation.priority_list = [
            ("Judgment", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.simulation = Simulation(self.paladin, self.targets, 40)
        self.simulation.priority_list = [
            ("Judgment", lambda: True),
        ]  
        
        # apply talents
        self.paladin.class_talents["row3"]["Greater Judgment"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row8"]["Judgment of Light"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row5"]["Justification"]["ranks"]["current rank"] = 1
        
        # recreate judgment
        self.paladin.abilities["Judgment"] = Judgment(self.paladin)
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
   
        # greater judgment
        self.assertNotIn("Greater Judgment", results_talent_inactive)
        self.assertIn("Greater Judgment applied", results_talent_active)
        self.assertTrue(
            "Greater Judgment absorbed" in results_talent_active or
            "Greater Judgment crit absorbed" in results_talent_active
        )
        self.assertIn("Greater Judgment removed", results_talent_active)
        
        # judgment of light
        self.assertNotIn("Judgment of Light", results_talent_inactive) 
        self.assertIn("Judgment of Light (5) applied", results_talent_active)
        self.assertTrue(
            "Judgment of Light healed" in results_talent_active or
            "Judgment of Light crit healed" in results_talent_active
        )
        self.assertIn("Judgment of Light removed", results_talent_active)
        
        # justification (10% judgment damage)
        judgment_damage_before = int(re.findall(r'\d+\.\d+: Judgment damaged \w+ for (\d+)', results_talent_inactive)[0])
        judgment_damage_after = int(re.findall(r'\d+\.\d+: Judgment damaged \w+ for (\d+)', results_talent_active)[0])
        self.assertEqual(round(judgment_damage_before * 1.1), judgment_damage_after)
   
    def test_touch_of_light(self):
        # return
        self.simulation = Simulation(self.paladin, self.targets, 300)
        self.simulation.priority_list = [
            ("Judgment", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.simulation = Simulation(self.paladin, self.targets, 300)
        self.simulation.priority_list = [
            ("Judgment", lambda: True),
        ]  
        
        # apply talents
        self.paladin.class_talents["row8"]["Touch of Light"]["ranks"]["current rank"] = 1
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertNotIn("Touch of Light", results_talent_inactive)
        self.assertTrue(
            "Touch of Light healed" in results_talent_active or
            "Touch of Light crit healed" in results_talent_active
        )   
   
    def test_afterimage(self):
        # return
        self.simulation = Simulation(self.paladin, self.targets, 50)
        self.simulation.priority_list = [
            ("Word of Glory", lambda: True),
            ("Flash of Light", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.simulation = Simulation(self.paladin, self.targets, 50)
        self.simulation.priority_list = [
            ("Word of Glory", lambda: True),
            ("Flash of Light", lambda: True),
        ]  
        
        # apply talents
        self.paladin.class_talents["row7"]["Afterimage"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row7"]["Tower of Radiance"]["ranks"]["current rank"] = 1
        
        # recreate tower of radiance spells
        self.paladin.abilities["Flash of Light"] = FlashOfLight(self.paladin)
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertNotIn("Afterimage", results_talent_inactive)
        self.assertIn("Afterimage", results_talent_active)
        
        # test light of dawn
        self.setUp()
        self.simulation = Simulation(self.paladin, self.targets, 50)
        
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row7"]["Afterimage"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row7"]["Tower of Radiance"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Word of Glory", lambda: self.simulation.elapsed_time > 40),
            ("Light of Dawn", lambda: True),
            ("Flash of Light", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertNotIn("Afterimage", results_talent_inactive)
        self.assertIn("Afterimage", results_talent_active)
   
    def test_holy_light_talents(self):
        # return
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Light", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        
        self.simulation.priority_list = [
            ("Divine Favor", lambda: True),
            ("Holy Light", lambda: True),
        ]  
        
        # apply talents
        self.paladin.spec_talents["row4"]["Awestruck"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row4"]["Resplendent Light"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row5"]["Divine Favor"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row7"]["Divine Revelations"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row7"]["Tower of Radiance"]["ranks"]["current rank"] = 1 
        self.paladin.load_abilities_based_on_talents()
        
        # recreate tower of radiance spells
        self.paladin.abilities["Holy Light"] = HolyLight(self.paladin)
        self.paladin.abilities["Divine Favor"] = DivineFavorSpell(self.paladin)
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # resplendent light
        self.assertNotIn("Resplendent Light healed", results_talent_inactive)
        self.assertIn("Resplendent Light healed", results_talent_active)
        
        # awestruck & divine favor
        holy_light_healing_none = int(re.findall(r'\d+\.\d+: Holy Light (?:crit )?healed \w+ for (\d+)', results_talent_inactive)[1])
        holy_light_healing_awestruck = int(re.findall(r'\d+\.\d+: Holy Light (?:crit )?healed \w+ for (\d+)', results_talent_active)[1])
        holy_light_healing_awestruck_divine_favor = int(re.findall(r'\d+\.\d+: Holy Light (?:crit )?healed \w+ for (\d+)', results_talent_active)[0])
        self.assertEqual(round(holy_light_healing_none * 1.1), holy_light_healing_awestruck)
        self.assertEqual(round(holy_light_healing_none * 1.1 * 1.6), holy_light_healing_awestruck_divine_favor)
        
        # compare cast times with divine favor
        holy_light_initial_cast_time_divine_favor_inactive = float(re.findall(r'(\d+\.\d+): Test Paladin started casting Holy Light', results_talent_inactive)[0])
        holy_light_final_cast_time_divine_favor_inactive = float(re.findall(r'(\d+\.\d+): Holy Light (?:crit )?healed \w+ for \d+', results_talent_inactive)[0])
        holy_light_divine_favor_inactive_cast_time = holy_light_final_cast_time_divine_favor_inactive - holy_light_initial_cast_time_divine_favor_inactive
        
        holy_light_initial_cast_time_divine_favor_active = float(re.findall(r'(\d+\.\d+): Test Paladin started casting Holy Light', results_talent_active)[0])
        holy_light_final_cast_time_divine_favor_active = float(re.findall(r'(\d+\.\d+): Holy Light (?:crit )?healed \w+ for \d+', results_talent_active)[0])
        holy_light_divine_favor_cast_time = holy_light_final_cast_time_divine_favor_active - holy_light_initial_cast_time_divine_favor_active
        self.assertEqual(round(holy_light_divine_favor_inactive_cast_time * 0.7, 2), holy_light_divine_favor_cast_time)
        
        # tower of radiance
        holy_light_holy_power_no_tower_of_radiance = re.findall(r'holy power before: (\d+)', results_talent_inactive)
        holy_light_holy_power_tower_of_radiance = re.findall(r'holy power before: (\d+)', results_talent_active)
        
        self.assertEqual(holy_light_holy_power_no_tower_of_radiance, [holy_light_holy_power_no_tower_of_radiance[0]] * len(holy_light_holy_power_no_tower_of_radiance))
        self.assertEqual(int(holy_light_holy_power_tower_of_radiance[0]) + 1, int(holy_light_holy_power_tower_of_radiance[1]))
        
    def test_flash_of_light_talents(self):
        # return
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Divine Favor", lambda: True),
            ("Holy Shock", lambda: self.simulation.elapsed_time <= 1),
            ("Flash of Light", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Divine Favor", lambda: True),
            ("Holy Shock", lambda: self.simulation.elapsed_time <= 1),
            ("Flash of Light", lambda: True),
        ]  
        
        # apply talents
        self.paladin.spec_talents["row4"]["Awestruck"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row5"]["Divine Favor"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row7"]["Divine Revelations"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row7"]["Tower of Radiance"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        # recreate tower of radiance spells
        self.paladin.abilities["Flash of Light"] = FlashOfLight(self.paladin)
        self.paladin.abilities["Divine Favor"] = DivineFavorSpell(self.paladin)
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # awestruck & divine revelations & divine favor
        flash_of_light_healing_before = int(re.findall(r'\d+\.\d+: Flash of Light (?:crit )?healed \w+ for (\d+)', results_talent_inactive)[0])
        flash_of_light_healing_after = int(re.findall(r'\d+\.\d+: Flash of Light (?:crit )?healed \w+ for (\d+)', results_talent_active)[0])
        self.assertEqual(round(flash_of_light_healing_before * 1.1 * 1.2 * 1.6), flash_of_light_healing_after)
        
        # compare cast times with divine favor
        flash_of_light_initial_cast_time_divine_favor_inactive = float(re.findall(r'(\d+\.\d+): Test Paladin started casting Flash of Light', results_talent_inactive)[0])
        flash_of_light_final_cast_time_divine_favor_inactive = float(re.findall(r'(\d+\.\d+): Flash of Light (?:crit )?healed \w+ for \d+', results_talent_inactive)[0])
        flash_of_light_divine_favor_inactive_cast_time = flash_of_light_final_cast_time_divine_favor_inactive - flash_of_light_initial_cast_time_divine_favor_inactive
        
        flash_of_light_initial_cast_time_divine_favor_active = float(re.findall(r'(\d+\.\d+): Test Paladin started casting Flash of Light', results_talent_active)[0])
        flash_of_light_final_cast_time_divine_favor_active = float(re.findall(r'(\d+\.\d+): Flash of Light (?:crit )?healed \w+ for \d+', results_talent_active)[0])
        flash_of_light_divine_favor_cast_time = flash_of_light_final_cast_time_divine_favor_active - flash_of_light_initial_cast_time_divine_favor_active
        self.assertTrue(abs(round(flash_of_light_divine_favor_inactive_cast_time * 0.7, 2) - round(flash_of_light_divine_favor_cast_time, 2)) < 0.02)
        
        # tower of radiance
        flash_of_light_holy_power_no_tower_of_radiance = re.findall(r'Flash of Light (?:crit )?healed \w+ for \d+, mana: \d+.\d+, holy power before: (\d+)', results_talent_inactive)
        flash_of_light_holy_power_tower_of_radiance = re.findall(r'Flash of Light (?:crit )?healed \w+ for \d+, mana: \d+.\d+, holy power before: (\d+)', results_talent_active)
        
        self.assertEqual(flash_of_light_holy_power_no_tower_of_radiance, [flash_of_light_holy_power_no_tower_of_radiance[0]] * len(flash_of_light_holy_power_no_tower_of_radiance))
        self.assertEqual(int(flash_of_light_holy_power_tower_of_radiance[0]) + 1, int(flash_of_light_holy_power_tower_of_radiance[1]))
        
    def test_holy_shock_talents(self):
        # return
        self.paladin.crit = 82
        self.simulation = Simulation(self.paladin, self.targets, 500)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        self.paladin.average_raid_health_percentage = 0.7
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True)
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 82
        self.simulation = Simulation(self.paladin, self.targets, 500)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
        ]  
        
        # apply talents
        self.paladin.spec_talents["row4"]["Awestruck"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row7"]["Divine Glimpse"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row8"]["Reclamation"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row10"]["Glorious Dawn"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        self.paladin.average_raid_health_percentage = 0.7
        
        self.paladin.abilities["Holy Shock"] = HolyShock(self.paladin)
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # awestruck & reclamation
        holy_shock_healing_before = int(re.findall(r'\d+\.\d+: Holy Shock crit healed \w+ for (\d+)', results_talent_inactive)[0])
        holy_shock_healing_after = int(re.findall(r'\d+\.\d+: Holy Shock crit healed \w+ for (\d+)', results_talent_active)[0])
        self.assertEqual(round(holy_shock_healing_before * 1.1 * 1.15), holy_shock_healing_after)
        
        # divine glimpse
        holy_shock_non_crits_before = len(re.findall(r'\d+\.\d+: Holy Shock healed \w+ for (\d+)', results_talent_inactive))
        holy_shock_non_crits_after = len(re.findall(r'\d+\.\d+: Holy Shock healed \w+ for (\d+)', results_talent_active))
        self.assertNotEqual(holy_shock_non_crits_before, holy_shock_non_crits_after)
        
        # glorious dawn
        holy_shock_resets_before = len(re.findall(r'\d+\.\d+: Holy Shock\'s cooldown was reset', results_talent_inactive))
        holy_shock_resets_after = len(re.findall(r'\d+\.\d+: Holy Shock\'s cooldown was reset', results_talent_active))
        self.assertTrue(holy_shock_resets_before == 0)
        self.assertTrue(holy_shock_resets_after > 0)
        
    def test_crusader_strike_talents(self):
        # return
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 5)
        self.paladin.load_abilities_based_on_talents()
        self.paladin.average_raid_health_percentage = 0.7
        
        # for reclamation
        self.paladin.average_raid_health_percentage = 1
        
        self.simulation.priority_list = [
            ("Crusader Strike", lambda: True)
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 5)
        
        self.simulation.priority_list = [
            ("Crusader Strike", lambda: True),
        ]  
        
        # apply talents
        self.paladin.class_talents["row7"]["Crusader's Reprieve"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row8"]["Reclamation"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        self.paladin.average_raid_health_percentage = 0.7
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reclamation
        crusader_strike_damage_before = int(re.findall(r'\d+\.\d+: Crusader Strike crit damaged \w+ for (\d+)', results_talent_inactive)[0])
        crusader_strike_damage_after = int(re.findall(r'\d+\.\d+: Crusader Strike crit damaged \w+ for (\d+)', results_talent_active)[0])
        self.assertEqual(round(crusader_strike_damage_before * 1.15) - 1, crusader_strike_damage_after)
        
        # crusader's reprieve
        self.assertNotIn("Crusader's Reprieve", results_talent_inactive)
        self.assertIn("Crusader's Reprieve", results_talent_active)
        
        crusaders_reprieve_heal = int(re.findall(r'\d+\.\d+: Crusader\'s Reprieve healed Test Paladin for (\d+)', results_talent_active)[0])
        self.assertEqual(crusaders_reprieve_heal, round(self.paladin.max_health * 0.02))
        
    def test_lights_conviction(self):
        # return
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True)
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        holy_shock_max_charges_before = HolyShock(self.paladin).max_charges
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
        ]  
        
        # apply talents
        self.paladin.spec_talents["row3"]["Light's Conviction"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        holy_shock_count_before = len(re.findall(r'\d+\.\d+: Holy Shock', results_talent_inactive))
        holy_shock_count_after = len(re.findall(r'\d+\.\d+: Holy Shock', results_talent_active))

        self.assertNotEqual(holy_shock_count_before, holy_shock_count_after)
        
        holy_shock_max_charges_after = HolyShock(self.paladin).max_charges
        self.assertNotEqual(holy_shock_max_charges_before, holy_shock_max_charges_after)
        
    def test_glimmer_of_light(self):
        # return
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Daybreak", lambda: self.simulation.elapsed_time >= 3),
            ("Divine Toll", lambda: True),
            ("Holy Shock", lambda: True)
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Daybreak", lambda: self.simulation.elapsed_time >= 3),
            ("Divine Toll", lambda: True),
            ("Holy Shock", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertNotIn("Glimmer of Light", results_talent_inactive)
        self.assertIn("Glimmer of Light", results_talent_active)
        
    def test_inflorescence_of_the_sunwell(self):
        # return
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 20)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        # self.paladin.spec_talents["row7"]["Divine Revelations"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Flash of Light", lambda: True)
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.simulation = Simulation(self.paladin, self.targets, 20)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Flash of Light", lambda: True)
        ]
        
        # apply talents
        self.paladin.spec_talents["row10"]["Inflorescence of the Sunwell"]["ranks"]["current rank"] = 1
        # self.paladin.spec_talents["row7"]["Divine Revelations"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertNotIn("Infusion of Light (2)", results_talent_inactive)
        self.assertIn("Infusion of Light (2)", results_talent_active)
        
    def test_imbued_infusions(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 1000)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        # self.paladin.spec_talents["row7"]["Divine Revelations"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Flash of Light", lambda: True)
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 1000)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Flash of Light", lambda: True)
        ]
        
        # apply talents
        self.paladin.spec_talents["row5"]["Imbued Infusions"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        holy_shock_count_before = len(re.findall(r'\d+\.\d+: Holy Shock crit healed \w+ for (\d+)', results_talent_inactive))
        holy_shock_count_after = len(re.findall(r'\d+\.\d+: Holy Shock crit healed \w+ for (\d+)', results_talent_active))
        
        # roughly 20% gain in holy shocks
        self.assertTrue(holy_shock_count_after > holy_shock_count_before * 1.19)
        
    def test_glistening_radiance(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 100)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.paladin.abilities["Word of Glory"].holy_power_cost = 0
        self.paladin.abilities["Light of Dawn"].holy_power_cost = 0
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: self.simulation.elapsed_time <= 1),
            ("Word of Glory", lambda: True),
            ("Light of Dawn", lambda: self.simulation.previous_ability == "Word of Glory")
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 100)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
        
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: self.simulation.elapsed_time <= 1),
            ("Word of Glory", lambda: True),
            ("Light of Dawn", lambda: self.simulation.previous_ability == "Word of Glory")
        ]
        
        # apply talents
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row5"]["Glistening Radiance"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.paladin.abilities["Word of Glory"].holy_power_cost = 0
        self.paladin.abilities["Light of Dawn"].holy_power_cost = 0
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertNotIn("Glimmer of Light", results_talent_inactive)
        self.assertIn("Glimmer of Light", results_talent_active)
        
    def test_divine_purpose(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 100)
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.paladin.abilities["Word of Glory"].holy_power_cost = 0
        self.paladin.abilities["Light of Dawn"].holy_power_cost = 0
        
        self.simulation.priority_list = [
            ("Word of Glory", lambda: True),
            ("Light of Dawn", lambda: self.simulation.previous_ability == "Word of Glory")
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 100)
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
        
        
        self.simulation.priority_list = [
            ("Word of Glory", lambda: True),
            ("Light of Dawn", lambda: self.simulation.previous_ability == "Word of Glory")
        ]
        
        # apply talents
        self.paladin.class_talents["row8"]["Divine Purpose"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.paladin.abilities["Word of Glory"].holy_power_cost = 0
        self.paladin.abilities["Light of Dawn"].holy_power_cost = 0
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))

        self.assertNotIn("Divine Purpose", results_talent_inactive)
        self.assertIn("Divine Purpose", results_talent_active)

    def test_overflowing_light(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
    
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Divine Toll", lambda: True),
            ("Daybreak", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Divine Toll", lambda: True),
            ("Daybreak", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row6"]["Overflowing Light"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))

        self.assertNotIn("Overflowing Light", results_talent_inactive)
        self.assertIn("Overflowing Light", results_talent_active)

    def test_of_dusk_and_dawn(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
    
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: self.simulation.elapsed_time <= 1),
            ("Divine Toll", lambda: self.simulation.elapsed_time <= 2),
            ("Holy Light", lambda: self.simulation.elapsed_time <= 4),
            ("Flash of Light", lambda: self.simulation.elapsed_time <= 6),
            ("Judgment", lambda: self.simulation.elapsed_time <= 7),
            ("Crusader Strike", lambda: self.simulation.elapsed_time <= 9),
            ("Word of Glory", lambda: self.simulation.elapsed_time <= 10),
            # ("Hammer of Wrath", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 10)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: self.simulation.elapsed_time <= 1),
            ("Divine Toll", lambda: self.simulation.elapsed_time <= 2),
            ("Holy Light", lambda: self.simulation.elapsed_time <= 4),
            ("Flash of Light", lambda: self.simulation.elapsed_time <= 6),
            ("Judgment", lambda: self.simulation.elapsed_time <= 7),
            ("Crusader Strike", lambda: self.simulation.elapsed_time <= 9),
            ("Word of Glory", lambda: self.simulation.elapsed_time <= 10),
            # ("Hammer of Wrath", lambda: True),
        ]
        
        # apply talents
        self.paladin.class_talents["row9"]["Of Dusk and Dawn"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))

        self.assertTrue(
            "Blessing of Dawn (1) applied" not in results_talent_inactive and
            "Blessing of Dawn (2) applied" not in results_talent_inactive and
            "Blessing of Dawn removed" not in results_talent_inactive and
            "Blessing of Dusk applied" not in results_talent_inactive
        )
        self.assertTrue(
            "Blessing of Dawn (1) applied" in results_talent_active and
            "Blessing of Dawn (2) applied" in results_talent_active and
            "Blessing of Dawn removed" in results_talent_active and
            "Blessing of Dusk applied" in results_talent_active
        )
        
    def test_seal_of_order(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 65)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
    
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Word of Glory", lambda: True),
            ("Holy Shock", lambda: True),
            ("Divine Toll", lambda: True),
            ("Judgment", lambda: True),
            ("Crusader Strike", lambda: self.simulation.elapsed_time >= 7),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 65)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Word of Glory", lambda: True),
            ("Holy Shock", lambda: True),
            ("Divine Toll", lambda: True),
            ("Judgment", lambda: True),
            ("Crusader Strike", lambda: self.simulation.elapsed_time >= 7),
        ]
        
        # apply talents
        self.paladin.class_talents["row9"]["Of Dusk and Dawn"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row10"]["Seal of Order"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        times_dusk_applied = re.findall(r'(\d+\.\d+): Blessing of Dusk applied', results_talent_active)
        first_time_dusk_applied = times_dusk_applied[0]
        
        holy_shock_times_before = re.findall(r'(\d+\.\d+): Holy Shock crit', results_talent_inactive)
        divine_toll_times_before = re.findall(r'(\d+\.\d+): Test Paladin cast Divine Toll', results_talent_inactive)
        judgment_times_before = re.findall(r'(\d+\.\d+): Judgment crit', results_talent_inactive)
        crusader_strike_times_before = re.findall(r'(\d+\.\d+): Crusader Strike crit', results_talent_inactive)
        
        holy_shock_times_after = re.findall(r'(\d+\.\d+): Holy Shock crit', results_talent_active)
        divine_toll_times_after = re.findall(r'(\d+\.\d+): Test Paladin cast Divine Toll', results_talent_active)
        judgment_times_after = re.findall(r'(\d+\.\d+): Judgment crit', results_talent_active)
        crusader_strike_times_after = re.findall(r'(\d+\.\d+): Crusader Strike crit', results_talent_active)
        
        print("Holy Shocks")
        print(holy_shock_times_before)
        print(holy_shock_times_after)
        
        print("Divine Tolls")
        print(divine_toll_times_before)
        print(divine_toll_times_after)
        
        print("Judgments")
        print(judgment_times_before)
        print(judgment_times_after)
        
        print("Crusader Strikes")
        print(crusader_strike_times_before)
        print(crusader_strike_times_after)
    
        self.assertTrue(float(holy_shock_times_before[1]) > float(holy_shock_times_after[1]))
        self.assertTrue(float(divine_toll_times_before[1]) > float(divine_toll_times_after[1]))
        self.assertTrue(float(judgment_times_before[1]) > float(judgment_times_after[1]))
        self.assertTrue(float(crusader_strike_times_before[1]) > float(crusader_strike_times_after[1]))

    def test_divine_resonance(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 20)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
    
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Divine Toll", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 20)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Divine Toll", lambda: True),
        ]
        
        # apply talents
        self.paladin.class_talents["row10"]["Divine Resonance"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertIn("Test Paladin cast Divine Toll", results_talent_inactive)
        divine_toll_holy_shock_count = len(re.findall(r'(\d+\.\d+): Holy Shock \(Divine Toll\)', results_talent_inactive))
        self.assertEqual(divine_toll_holy_shock_count, 5)
        self.assertNotIn("Holy Shock (Divine Resonance)", results_talent_inactive)
        
        self.assertIn("Test Paladin cast Divine Toll", results_talent_active)
        divine_toll_holy_shock_count = len(re.findall(r'(\d+\.\d+): Holy Shock \(Divine Toll\)', results_talent_active))
        self.assertEqual(divine_toll_holy_shock_count, 5)
        self.assertIn("Holy Shock (Divine Resonance)", results_talent_active)
        divine_resonance_holy_shock_count = len(re.findall(r'(\d+\.\d+): Holy Shock \(Divine Resonance\)', results_talent_active))
        self.assertEqual(divine_resonance_holy_shock_count, 3)
        
    def test_quickened_invocation(self):
        # return
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 65)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
    
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Divine Toll", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 100
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 65)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Divine Toll", lambda: True),
        ]
        
        # apply talents
        self.paladin.class_talents["row10"]["Quickened Invocation"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertIn("Test Paladin cast Divine Toll", results_talent_inactive)
        divine_toll_holy_shock_count = len(re.findall(r'(\d+\.\d+): Holy Shock \(Divine Toll\)', results_talent_inactive))
        self.assertEqual(divine_toll_holy_shock_count, 10)
        divine_toll_times_before = re.findall(r'(\d+\.\d+): Test Paladin cast Divine Toll', results_talent_inactive)
        
        self.assertIn("Test Paladin cast Divine Toll", results_talent_active)
        divine_toll_holy_shock_count = len(re.findall(r'(\d+\.\d+): Holy Shock \(Divine Toll\)', results_talent_active))
        self.assertEqual(divine_toll_holy_shock_count, 10)
        divine_toll_times_after = re.findall(r'(\d+\.\d+): Test Paladin cast Divine Toll', results_talent_active)
        
        print("Divine Tolls")
        print(divine_toll_times_before)
        print(divine_toll_times_after)
        
        self.assertTrue(float(divine_toll_times_before[1]) - float(divine_toll_times_after[1]) == 15)

    def test_avenging_wrath_might(self):
        # return
        self.paladin.crit = 85
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 500)
        self.paladin.class_talents["row5"]["Avenging Wrath"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        self.paladin.abilities["Avenging Wrath"].cooldown = 20
        
        self.simulation.priority_list = [
            ("Avenging Wrath", lambda: True),
            ("Holy Shock", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 85
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 500)
        self.paladin.class_talents["row5"]["Avenging Wrath"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Avenging Wrath", lambda: True),
            ("Holy Shock", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row8"]["Avenging Wrath: Might"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        self.paladin.abilities["Avenging Wrath"].cooldown = 20
        
        self.simulation.simulate()
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        holy_shock_non_crits_before = len(re.findall(r'\d+\.\d+: Holy Shock healed \w+ for (\d+)', results_talent_inactive))
        print(holy_shock_non_crits_before)
        holy_shock_non_crits_after = len(re.findall(r'\d+\.\d+: Holy Shock healed \w+ for (\d+)', results_talent_active))
        print(holy_shock_non_crits_after)
        self.assertNotEqual(holy_shock_non_crits_before, holy_shock_non_crits_after)

    def test_awakening(self):
        # # return
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 75)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        self.paladin.abilities["Crusader Strike"].cooldown = 0
        
        self.simulation.priority_list = [
            ("Judgment", lambda: "Awakening READY!!!!!!" in self.paladin.active_auras),
            ("Word of Glory", lambda: True),
            ("Judgment", lambda: True),
            ("Crusader Strike", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 75)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Judgment", lambda: "Awakening READY!!!!!!" in self.paladin.active_auras),
            ("Word of Glory", lambda: True),
            ("Judgment", lambda: True),
            ("Crusader Strike", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row10"]["Awakening"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        self.paladin.abilities["Crusader Strike"].cooldown = 0
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        for i in range(12):
            self.assertNotIn(f"Awakening ({i + 1})", results_talent_inactive)  
        self.assertNotIn("Awakening READY!!!!!!", results_talent_inactive)
        judgment_damage_before = int(re.findall(r'(\d+\.\d+): Judgment (?:crit )?damaged \w+ for (\d+)', results_talent_inactive)[6][1])
          
        for i in range(12):
            self.assertIn(f"Awakening ({i + 1})", results_talent_active) 
        self.assertIn("Awakening READY!!!!!!", results_talent_active)
        judgment_damage_after = int(re.findall(r'(\d+\.\d+): Judgment (?:crit )?damaged \w+ for (\d+)', results_talent_active)[6][1])

        print(self.paladin.crit)
        self.assertEqual(round(judgment_damage_before * 2 * 1.3), judgment_damage_after)
        
        self.paladin.abilities["Crusader Strike"].cooldown = 7.75

    def test_boundless_salvation(self):
        # return
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 75)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Tyr's Deliverance"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Tyr's Deliverance", lambda: True),
            ("Holy Light", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        # HOLY LIGHT
        self.setUp()
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 75)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Tyr's Deliverance"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Tyr's Deliverance", lambda: True),
            ("Holy Light", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row10"]["Boundless Salvation"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        tyrs_deliverance_times_applied_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) applied', results_talent_inactive)
        tyrs_deliverance_times_removed_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) removed', results_talent_inactive)
        tyrs_deliverance_times_extended_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) extended', results_talent_inactive)
        
        tyrs_deliverance_times_applied_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) applied', results_talent_active)
        tyrs_deliverance_times_removed_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) removed', results_talent_active)
        tyrs_deliverance_times_extended_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) extended', results_talent_active)
        
        print("Times removed: Holy Light")
        print(tyrs_deliverance_times_removed_before)
        print(tyrs_deliverance_times_removed_after)
        self.assertAlmostEqual(round(float(tyrs_deliverance_times_removed_after[0]) - float(tyrs_deliverance_times_removed_before[0])), 40)
        self.assertAlmostEqual(round(float(tyrs_deliverance_times_removed_after[0]) - float(tyrs_deliverance_times_removed_before[0])) % 8, 0)
        
        print("Times extended: Holy Light")
        print(tyrs_deliverance_times_extended_before)
        self.assertEqual(len(tyrs_deliverance_times_extended_before), 0)
        print(tyrs_deliverance_times_extended_after)
        self.assertEqual(len(tyrs_deliverance_times_extended_after), 5)
        
        # FLASH OF LIGHT
        self.setUp()
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 75)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Tyr's Deliverance"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Tyr's Deliverance", lambda: True),
            ("Flash of Light", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row10"]["Boundless Salvation"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        tyrs_deliverance_times_applied_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) applied', results_talent_inactive)
        tyrs_deliverance_times_removed_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) removed', results_talent_inactive)
        tyrs_deliverance_times_extended_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) extended', results_talent_inactive)
        
        tyrs_deliverance_times_applied_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) applied', results_talent_active)
        tyrs_deliverance_times_removed_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) removed', results_talent_active)
        tyrs_deliverance_times_extended_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) extended', results_talent_active)
        
        print("Times removed: Flash of Light")
        print(tyrs_deliverance_times_removed_before)
        print(tyrs_deliverance_times_removed_after)
        self.assertAlmostEqual(round(float(tyrs_deliverance_times_removed_after[0]) - float(tyrs_deliverance_times_removed_before[0])), 40)
        self.assertAlmostEqual(round(float(tyrs_deliverance_times_removed_after[0]) - float(tyrs_deliverance_times_removed_before[0])) % 4, 0)
        
        print("Times extended: Flash of Light")
        print(tyrs_deliverance_times_extended_before)
        self.assertEqual(len(tyrs_deliverance_times_extended_before), 0)
        print(tyrs_deliverance_times_extended_after)
        self.assertEqual(len(tyrs_deliverance_times_extended_after), 10)
        
        # HOLY SHOCK
        self.setUp()
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 75)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Tyr's Deliverance"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Tyr's Deliverance", lambda: True),
            ("Holy Shock", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row10"]["Boundless Salvation"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        tyrs_deliverance_times_applied_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) applied', results_talent_inactive)
        tyrs_deliverance_times_removed_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) removed', results_talent_inactive)
        tyrs_deliverance_times_extended_before = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) extended', results_talent_inactive)
        
        tyrs_deliverance_times_applied_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) applied', results_talent_active)
        tyrs_deliverance_times_removed_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) removed', results_talent_active)
        tyrs_deliverance_times_extended_after = re.findall(r'(\d+\.\d+): Tyr\'s Deliverance \(self\) extended', results_talent_active)
        
        print("Times removed: Holy Shock")
        print(tyrs_deliverance_times_removed_before)
        print(tyrs_deliverance_times_removed_after)
        self.assertAlmostEqual(round(float(tyrs_deliverance_times_removed_after[0]) - float(tyrs_deliverance_times_removed_before[0])) % 2, 0)
        
        print("Times extended: Holy Shock")
        print(tyrs_deliverance_times_extended_before)
        self.assertEqual(len(tyrs_deliverance_times_extended_before), 0)
        print(tyrs_deliverance_times_extended_after)

    def test_illumination(self):
        # return
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 15)
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row10"]["Divine Resonance"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Divine Toll", lambda: True),
            ("Holy Shock", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = 0
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 15)
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row10"]["Divine Resonance"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Divine Toll", lambda: True),
            ("Holy Shock", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row6"]["Illumination"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        times_glimmer_removed_before = re.findall(r'(\d+\.\d+): Glimmer of Light removed', results_talent_inactive)
        times_glimmer_removed_after = re.findall(r'(\d+\.\d+): Glimmer of Light removed', results_talent_active)
        
        self.assertEqual(len(times_glimmer_removed_before) - len(times_glimmer_removed_after), 5)

    def test_ability_talents(self):
        # return
        self.paladin.crit = -10
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 15)
        
        self.paladin.load_abilities_based_on_talents()
        self.paladin.abilities["Holy Light"] = HolyLight(self.paladin)
           
        self.simulation.priority_list = [
            ("Avenging Wrath", lambda: True),
            ("Divine Favor", lambda: True),
            ("Light of Dawn", lambda: self.paladin.holy_power == 5),
            ("Divine Toll", lambda: True),
            ("Light's Hammer", lambda: True),
            ("Tyr's Deliverance", lambda: True),
            ("Blessing of the Seasons", lambda: True),
            ("Holy Shock", lambda: True),
            ("Daybreak", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = -10
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 50)
        self.paladin.class_talents["row5"]["Avenging Wrath"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row9"]["Divine Toll"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Light of Dawn"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row5"]["Divine Favor"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row6"]["Light's Hammer"]["ranks"]["current rank"] = 1  
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Tyr's Deliverance"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Blessing of Summer"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Avenging Wrath", lambda: True),
            ("Divine Favor", lambda: True),
            ("Light of Dawn", lambda: self.paladin.holy_power == 5),
            ("Divine Toll", lambda: True),
            ("Light's Hammer", lambda: True),
            ("Tyr's Deliverance", lambda: True),
            ("Blessing of the Seasons", lambda: True),
            ("Holy Shock", lambda: True),
            ("Daybreak", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        self.paladin.abilities["Holy Light"] = HolyLight(self.paladin)
        self.paladin.abilities["Divine Favor"] = DivineFavorSpell(self.paladin)
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertTrue(
            "Avenging Wrath" not in results_talent_inactive and
            "Divine Favor" not in results_talent_inactive and
            "Light of Dawn" not in results_talent_inactive and
            "Divine Toll" not in results_talent_inactive and
            "Light's Hammer" not in results_talent_inactive and
            "Tyr's Deliverance" not in results_talent_inactive and
            "Blessing of Summer" not in results_talent_inactive and
            "Holy Shock" not in results_talent_inactive and
            "Daybreak" not in results_talent_inactive and
            "Divine Favor" not in results_talent_inactive
        )
        
        self.assertTrue(
            "Avenging Wrath" in results_talent_active and
            "Divine Favor" in results_talent_active and
            "Light of Dawn" in results_talent_active and
            "Divine Toll" in results_talent_active and
            "Light's Hammer" in results_talent_active and
            "Tyr's Deliverance" in results_talent_active and
            "Blessing of Summer" in results_talent_active and
            "Holy Shock" in results_talent_active and
            "Daybreak" in results_talent_active and
            "Divine Favor" in results_talent_active
        )

    def test_blessing_of_the_seasons(self):
        # return
        self.paladin.crit = -10
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 210)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Blessing of Summer"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Blessing of the Seasons", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = -10
        self.paladin.mana = 200000
        self.paladin.mana_regen_per_second = 0
        self.simulation = Simulation(self.paladin, self.targets, 210)
        self.paladin.class_talents["row9"]["Of Dusk and Dawn"]["ranks"]["current rank"] = 1
        self.paladin.class_talents["row10"]["Seal of Order"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Blessing of Summer"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Blessing of the Seasons", lambda: True),
            ("Word of Glory", lambda: 46 < self.simulation.elapsed_time < 47),
            ("Holy Shock", lambda: "Blessing of Winter" not in self.paladin.active_auras),
        ]
        
        # apply talents
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        self.assertTrue(
            "Blessing of Summer" in results_talent_active and
            "Blessing of Autumn" in results_talent_active and
            "Blessing of Winter" in results_talent_active and
            "Blessing of Spring" in results_talent_active
        )
        
        # autumn
        holy_shock_times = re.findall(r'(\d+\.\d+): Holy Shock (?:crit )?healed \w+ for \d+', results_talent_active)
        print(holy_shock_times)
        autumn_and_dusk_holy_shock_cooldown = float(holy_shock_times[8]) - float(holy_shock_times[7])
        self.assertAlmostEqual(round(autumn_and_dusk_holy_shock_cooldown, 2), round(HolyShock(self.paladin).calculate_cooldown(self.paladin) / (1 + 0.3 + 0.1), 2))
        
        # spring
        holy_shock_heals = re.findall(r'\d+\.\d+: Holy Shock (?:crit )?healed \w+ for (\d+)', results_talent_active)
        self.assertAlmostEqual(int(holy_shock_heals[17]), round(int(holy_shock_heals[0]) * 1.15))
        
        # winter
        mana_gained = re.findall(r'\d+\.\d+: \w+\s?\w+? gained (\d+) mana from Blessing of Winter', results_talent_active)
        self.assertEqual(int(mana_gained[0]), int(self.paladin.base_mana * 0.01 * 15))

    def test_rising_sunlight(self):
        # return
        self.paladin.crit = -10
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 30)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Daybreak", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = -10
        self.paladin.mana = 200000
        self.paladin.mana_regen_per_second = 0
        self.simulation = Simulation(self.paladin, self.targets, 30)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Daybreak", lambda: True),
        ]
        
        # apply talents
        self.paladin.spec_talents["row10"]["Rising Sunlight"]["ranks"]["current rank"] = 1
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        holy_shock_times_before = re.findall(r'(\d+\.\d+): Holy Shock (?:\(Rising Sunlight\) )?healed \w+ for \d+', results_talent_inactive)
        holy_shock_times_after = re.findall(r'(\d+\.\d+): Holy Shock (?:\(Rising Sunlight\) )?healed \w+ for \d+', results_talent_active)
        self.assertEqual(len(holy_shock_times_before) + 6, len(holy_shock_times_after))

    def test_first_light(self):
        # return
        self.paladin.crit = -10
        self.paladin.mana_regen_per_second = 20000
        self.simulation = Simulation(self.paladin, self.targets, 21)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Daybreak", lambda: True),
        ]  
        
        self.simulation.simulate()
        results_talent_inactive = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # reset simulation
        self.setUp()
        self.paladin.crit = -10
        self.paladin.mana = 200000
        self.paladin.mana_regen_per_second = 0
        self.simulation = Simulation(self.paladin, self.targets, 21)
        self.paladin.spec_talents["row1"]["Holy Shock"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row2"]["Glimmer of Light"]["ranks"]["current rank"] = 1
        self.paladin.spec_talents["row9"]["Daybreak"]["ranks"]["current rank"] = 1
        
        self.simulation.priority_list = [
            ("Holy Shock", lambda: True),
            ("Daybreak", lambda: True),
        ]
        
        # apply talents
        self.paladin.load_abilities_based_on_talents()
        
        self.simulation.simulate()
        
        results_talent_active = "\n".join(self.simulation.test_healing_and_buff_events(self.targets))
        
        # making sure haste updates hasted cooldowns dynamically
        holy_shock_times_before = re.findall(r'(\d+\.\d+): Holy Shock (?:\(Rising Sunlight\) )?healed \w+ for \d+', results_talent_inactive)
        holy_shock_times_after = re.findall(r'(\d+\.\d+): Holy Shock (?:\(Rising Sunlight\) )?healed \w+ for \d+', results_talent_active)
        print(holy_shock_times_before)
        print(holy_shock_times_after)
        
        calculated_cooldown = (1.5 / 1.2298) + (8.5 / 1.5375) - 1.22 * ((8.5 / 1.5375) / (8.5 / 1.2298))
        print(calculated_cooldown)
        self.assertAlmostEqual(float(holy_shock_times_after[1]), round(calculated_cooldown, 2) + 0.01)

if __name__ == "__main__":
    unittest.main()