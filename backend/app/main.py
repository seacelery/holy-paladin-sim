# DO NEXT
# fix
# append each sim at the top of the list, make collapsible
# mana, holy power, glimmer, tyrs targets graphs

# awakening cancelaura
# movement every so often
# breakdowns in cooldown windows

# commanding light

# known issues
# glorious dawn calculation before or after glimmer application - currently assuming before
# assuming afterimage cannot proc divine purpose or glistening radiance after testing
# seal of might gives 3% mastery per point for reasons??
# light's hammer bad fix on casts vs hits
# it's slow
# touch of light weird rppm interaction?
# reset priority on tab swap to remove lag

# options to include
# heals on beacons, light of dawn targets hit, resplendent, mastery effectiveness, overheal for overflowing and reclamation

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
    
def initialise_simulation(paladin, healing_targets, encounter_length, iterations, time_warp_time, priority_list=None, custom_equipment=None):
    simulation = Simulation(paladin, healing_targets, encounter_length, iterations, time_warp_time, priority_list, custom_equipment, access_token)
    return simulation

def fetch_updated_data(paladin):
    return paladin
    
def run_simulation(simulation):
    return simulation.display_results()
    
if __name__ == "__main__":
    paladin, healing_targets = import_character("daisu", "aszune")
    
    simulation = initialise_simulation(paladin, healing_targets, encounter_length=30, iterations=1, time_warp_time=0)
    run_simulation(simulation)
