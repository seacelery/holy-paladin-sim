from . import battlenet_api
from functools import cache

@cache
def cached_get_character_data(access_token, realm, character_name, region):
    return battlenet_api.get_character_data(access_token, realm, character_name, region)

@cache
def cached_get_talent_data(access_token, realm, character_name, region):
    return battlenet_api.get_talent_data(access_token, realm, character_name, region)

@cache
def cached_get_stats_data(access_token, stats_url):
    return battlenet_api.get_stats_data(access_token, stats_url)

@cache
def cached_get_equipment_data(access_token, equipment_url):
    return battlenet_api.get_equipment_data(access_token, equipment_url)

@cache
def cached_get_spell_icon_data(access_token, spell_id):
    return battlenet_api.get_spell_icon_data(access_token, spell_id)

def clear_all_caches():
    cached_get_character_data.cache_clear()
    cached_get_talent_data.cache_clear()
    cached_get_stats_data.cache_clear()
    cached_get_equipment_data.cache_clear()