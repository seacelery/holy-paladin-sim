# DO NEXT
# fix
# light's hammer & prism, aura mastery, consecrate, hammer of wrath, light of the martyr, barrier of faith, virtue, melee wings, summer
# divine purpose, dusk and dawn, afterimage, glorious dawn, reclamation, revelations, resplendent light, golden path, crusader's reprieve, moment of compassion
# seal of mercy, strength of conviction, incandescence, touch of light, seal of order, fading light, seal of the crusader, vanguard's momentum, tirion's devotion
# unending light, awestruck, holy infusion, hand of divinity, glistening radiance, imbued infusions, single glimmer, saved by the light, power of the silver hand
# maraads, overflowing light, righteous judgment, veneration, crusader's might, aura of mercy, relentless inquisitor, boundless salvation, empyrean legacy, sanctified wrath
# stat bonuses - holy aegis, seal of alacrity, seal of might, judge damage, judge cdr
# AND make sure everything is only active when the talent is active

# actual build:
#  ̶j̶u̶d̶g̶e̶ ̶d̶a̶m̶a̶g̶e̶, holy aegis, afterimage, ̶c̶r̶u̶s̶a̶d̶e̶r̶'̶s̶ ̶r̶e̶p̶r̶i̶e̶v̶e̶, seal of might, ̶d̶i̶v̶i̶n̶e̶ ̶p̶u̶r̶p̶o̶s̶e, ̶s̶e̶a̶l̶ ̶o̶f̶ ̶a̶l̶a̶c̶r̶i̶t̶y̶ ̶c̶d̶r̶, ̶t̶o̶u̶c̶h̶ ̶o̶f̶ ̶l̶i̶g̶h̶t̶, ̶d̶u̶s̶k̶ ̶a̶n̶d̶ ̶d̶a̶w̶n̶, ̶s̶e̶a̶l̶ ̶o̶f̶ ̶o̶r̶d̶e̶r̶
#  ̶a̶w̶e̶s̶t̶r̶u̶c̶k, ̶r̶e̶s̶p̶l̶e̶n̶d̶e̶n̶t̶ ̶l̶i̶g̶h̶t̶, ̶g̶l̶i̶s̶t̶e̶n̶i̶n̶g̶ ̶r̶a̶d̶i̶a̶n̶c̶e̶, i̶m̶b̶u̶e̶d̶ ̶i̶n̶f̶u̶s̶i̶o̶n̶s, ̶l̶i̶g̶h̶t̶'̶s̶ ̶h̶a̶m̶m̶e̶r, ̶o̶v̶e̶r̶f̶l̶o̶w̶i̶n̶g̶ ̶l̶i̶g̶h̶t̶, ̶r̶e̶v̶e̶l̶a̶t̶i̶o̶n̶s, ̶r̶e̶c̶l̶a̶m̶a̶t̶i̶o̶n̶, ̶g̶l̶o̶r̶i̶o̶u̶s̶ ̶d̶a̶w̶n, summer
#
# awakening cancelaura
# movement every so often
# breakdowns in cooldown windows

# TALENT CHECKLIST
# CLASS tree
# greater judgment d
# holy aegis d
# judge damage d
# afterimage d
# crusader's reprieve d
# judgment of light d
# seal of might d
# divine purpose d
# seal of alacrity d
# touch of light d
# of dusk and dawn d
# divine toll d
# seal of order d
# divine resonance d
# quickened invocation d

# SPEC tree
# glimmer of light d
# light's conviction d
# resplendent light d
# awestruck d
# divine favor d
# glistening radiance d
# imbued infusions d
# illumination d
# overflowing light d
# divine revelations d
# commanding light
# tower of radiance d
# divine glimpse d
# avenging wrath: might d
# reclamation d
# daybreak d
# blessing of summer d
# rising sunlight d
# glorious dawn d
# inflorescence of the sunwell d
# awakening d
# boundless salvation d



# known issues
# light of dawn spends mana on each target - move the mana out of cast spell into the cast success
# glorious dawn calculation before or after glimmer application - currently assuming before
# assuming afterimage cannot proc divine purpose or glistening radiance after testing
# crusader strike uses attack power not sp
# seal of might gives 3% mastery per point for reasons??

# options to include
# heals on beacons, light of dawn targets hit

from simulation import Simulation
from paladin import Paladin
from target import Target, BeaconOfLight
import battlenet_api
import cache
import pprint
pp = pprint.PrettyPrinter(width=200)

client_id = "57cdb961fae04b8f9dc4d3caea3716db"
client_secret = "y3TJQqhljQ7fp50BWMLlvEoIr7yrfxBg"
access_token = battlenet_api.get_access_token(client_id, client_secret)

def main():
    healing_targets = [Target(f"target{i + 1}") for i in range(18)] + [BeaconOfLight(f"beaconTarget{i + 1}") for i in range(2)]
    beacon_targets = [target for target in healing_targets if isinstance(target, BeaconOfLight)]
    paladin = Paladin(character_name, character_data, stats_data, talent_data=talent_data, equipment_data=equipment_data, potential_healing_targets=healing_targets)
    paladin.set_beacon_targets(beacon_targets)
    simulation = Simulation(paladin, healing_targets, 30)
    simulation.simulate()
    simulation.display_results(healing_targets)
    
if __name__ == "__main__":
    realm = 'aszune'
    character_name = 'daisu'
    # realm = 'twisting-nether'
    # character_name = 'skaneschnell'
    
    character_data = cache.cached_get_character_data(access_token, realm, character_name)
    stats_data = cache.cached_get_stats_data(access_token, character_data["statistics"]["href"])
    equipment_data = cache.cached_get_equipment_data(access_token, character_data["equipment"]["href"])
    talent_data = cache.cached_get_talent_data(access_token, realm, character_name)
    
    main()
    
    # from collections import Counter
    
    # result_counter = Counter()
    
    # for i in range(10000):
    #     print(i)
    #     result_counter.update(main())
        
    # print(result_counter)