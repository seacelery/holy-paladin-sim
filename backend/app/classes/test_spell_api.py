import requests

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
    url = f"https://eu.api.blizzard.com/data/wow/item/{item_id}?locale=en_GB&access_token={access_token}&namespace=static-10.2.0_51825-eu"
    response = requests.get(url)
    return response.json()

def get(access_token, url_start):
    url = url_start + f"&local=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()
    

client_id = "57cdb961fae04b8f9dc4d3caea3716db"
client_secret = "rIIdFk2In9dQfBUxbPmH6ee4DDDO6oUV"
access_token = get_access_token(client_id, client_secret)

spell_ids = [200482]
for id in spell_ids:
    icon = get_spell_icon_data(access_token, id)
    print(icon)

# achievement_ids = [8845]
# for id in achievement_ids:
#     achievement = get_achievement_icon_data(access_token, id)
#     print(achievement)

# print(get_spell_info(access_token, 53576))

# print(get_item_info(access_token, 210692))
# print(get(access_token, "https://eu.api.blizzard.com/data/wow/media/item/210692?namespace=static-10.2.0_51825-eu"))