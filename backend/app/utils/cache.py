from utils import battlenet_api
from functools import cache

@cache
def cached_get_character_data(access_token, realm, character_name):
    return battlenet_api.get_character_data(access_token, realm, character_name)

@cache
def cached_get_talent_data(access_token, realm, character_name):
    return battlenet_api.get_talent_data(access_token, realm, character_name)

@cache
def cached_get_stats_data(access_token, stats_url):
    return battlenet_api.get_stats_data(access_token, stats_url)

@cache
def cached_get_equipment_data(access_token, equipment_url):
    return battlenet_api.get_equipment_data(access_token, equipment_url)