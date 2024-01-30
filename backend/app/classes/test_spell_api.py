import requests
import pprint

pp = pprint.PrettyPrinter(width=200)

def get_access_token(client_id, client_secret):
    url = "https://eu.battle.net/oauth/token"
    response = requests.post(url, data={'grant_type': 'client_credentials'}, auth=(client_id, client_secret))
    return response.json()["access_token"]

def get_spell_icon_data(access_token, spellId):
    url = f'https://eu.api.blizzard.com/data/wow/achievement/{spellId}?locale=en_GB&access_token={access_token}&namespace=static-eu'
    response = requests.get(url)
    return response.json()

def get_achievement_icon_data(access_token, achievementId):
    url = f"https://eu.api.blizzard.com/data/wow/media/achievement/{achievementId}?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu"
    response = requests.get(url)
    return response.json()

def get_spell_info(access_token, id):
    url = f"https://eu.api.blizzard.com/data/wow/spell/{id}?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu"
    response = requests.get(url)
    return response.json()

def get_icon_from_spell_info(access_token, id):
    url = f"https://eu.api.blizzard.com/data/wow/media/spell/{id}?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu"
    response = requests.get(url)
    return response.json()

def get_item_info(access_token, item_id):
    url = f"https://eu.api.blizzard.com/data/wow/media/item/{item_id}?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu"
    response = requests.get(url)
    return response.json()

# def get_item_info(access_token, item_id):
#     url = f"https://eu.api.blizzard.com/data/wow/search/item?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu&item=smoldering-seedling"
#     response = requests.get(url)
#     return response.json()

def get_race_info(access_token, playableRaceId=None):
    url = f"https://eu.api.blizzard.com/data/wow/playable-race/index?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu"
    response = requests.get(url)
    return response.json()

def get_specific_race_info(access_token, playableRaceId):
    url = f"https://eu.api.blizzard.com/data/wow/playable-race/{playableRaceId}?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu"
    response = requests.get(url)
    return response.json()


def get(access_token, url_start):
    url = url_start + f"&local=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()
    

client_id = "57cdb961fae04b8f9dc4d3caea3716db"
client_secret = "rIIdFk2In9dQfBUxbPmH6ee4DDDO6oUV"
access_token = get_access_token(client_id, client_secret)

# spell_ids = [20473,85222,85673,287269,375576,53563,82326,19750,114158,35395,20271,414127,392902,403042,183778,231644,385349,]
# for id in spell_ids:
#     icon = get_icon_from_spell_info(access_token, id)
#     print(icon)
    
pp.pprint(get_race_info(access_token))#
pp.pprint(get_specific_race_info(access_token, 30))

# pp.pprint(get(access_token, 'https://eu.api.blizzard.com/data/wow/playable-race/30?namespace=static-10.2.0_51825-eu'))

# achievement_ids = [8845]
# for id in achievement_ids:
#     achievement = get_achievement_icon_data(access_token, id)
#     print(achievement)

# print(get_spell_info(access_token, 53576))

# pp.pprint(get_item_info(access_token, 207170))
# print(get(access_token, "https://eu.api.blizzard.com/data/wow/media/item/210692?namespace=static-10.2.0_51825-eu"))