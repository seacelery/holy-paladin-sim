import requests
import pprint
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

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
    
def get_item_media(access_token, url_start):
    url = url_start + f"&local=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()

access_token = get_access_token(client_id, client_secret)

pp.pprint(get_item_media(access_token, "https://eu.api.blizzard.com/data/wow/media/item/195475?namespace=static-10.2.5_52554-eu"))
    
# pp.pprint(get_race_info(access_token))#
# pp.pprint(get_specific_race_info(access_token, 30))

# pp.pprint(get(access_token, 'https://eu.api.blizzard.com/data/wow/playable-race/30?namespace=static-10.2.0_51825-eu'))

# achievement_ids = [8845]
# for id in achievement_ids:
#     achievement = get_achievement_icon_data(access_token, id)
#     print(achievement)

# print(get_spell_info(access_token, 53576))

# pp.pprint(get_item_info(access_token, 207170))
# print(get(access_token, "https://eu.api.blizzard.com/data/wow/media/item/210692?namespace=static-10.2.0_51825-eu"))