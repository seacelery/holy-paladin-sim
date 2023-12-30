# DO NEXT
# fix
# light's hammer & prism, aura mastery, consecrate, hammer of wrath, light of the martyr, barrier of faith, virtue, melee wings, summer
# divine purpose, dusk and dawn, afterimage, glorious dawn, reclamation, revelations, resplendent light, golden path, crusader's reprieve, moment of compassion
# seal of mercy, strength of conviction, incandescence, touch of light, seal of order, fading light, seal of the crusader, vanguard's momentum, tirion's devotion
# unending light, awestruck, holy infusion, hand of divinity, glistening radiance, imbued infusions, single glimmer, saved by the light, power of the silver hand
# maraads, overflowing light, righteous judgment, veneration, crusader's might, aura of mercy, relentless inquisitor, boundless salvation, empyrean legacy, sanctified wrath

# awakening cancelaura
# movement every so often
# breakdowns in cooldown windows

# commanding light

# known issues
# glorious dawn calculation before or after glimmer application - currently assuming before
# assuming afterimage cannot proc divine purpose or glistening radiance after testing
# seal of might gives 3% mastery per point for reasons??
# light's hammer bad fix on casts vs hits

# options to include
# heals on beacons, light of dawn targets hit

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pprint

from app.classes.simulation import Simulation
from app.classes.paladin import Paladin
from app.classes.target import Target, BeaconOfLight
from app.utils import cache, battlenet_api

pp = pprint.PrettyPrinter(width=200)

client_id = "57cdb961fae04b8f9dc4d3caea3716db"
client_secret = "rIIdFk2In9dQfBUxbPmH6ee4DDDO6oUV"
access_token = battlenet_api.get_access_token(client_id, client_secret)


def import_character(character_name, realm):
    character_data = cache.cached_get_character_data(access_token, realm, character_name)
    stats_data = cache.cached_get_stats_data(access_token, character_data["statistics"]["href"])
    equipment_data = cache.cached_get_equipment_data(access_token, character_data["equipment"]["href"])
    talent_data = cache.cached_get_talent_data(access_token, realm, character_name)
    
    healing_targets = [Target(f"target{i + 1}") for i in range(18)] + [BeaconOfLight(f"beaconTarget{i + 1}") for i in range(2)]
    beacon_targets = [target for target in healing_targets if isinstance(target, BeaconOfLight)]
    
    paladin = Paladin(character_name, character_data, stats_data, talent_data=talent_data, equipment_data=equipment_data, potential_healing_targets=healing_targets)
    paladin.set_beacon_targets(beacon_targets)
    
    return paladin, healing_targets
    
def run_simulation(paladin, healing_targets):
    simulation = Simulation(paladin, healing_targets, 65, access_token)
    simulation.simulate()
    
    return simulation.display_results(healing_targets)
    
if __name__ == "__main__":
    paladin, healing_targets = import_character("daisu", "aszune")
    run_simulation(paladin, healing_targets)
