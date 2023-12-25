import requests

def get_access_token(client_id, client_secret):
    url = "https://eu.battle.net/oauth/token"
    response = requests.post(url, data={'grant_type': 'client_credentials'}, auth=(client_id, client_secret))
    return response.json()["access_token"]

def get_character_data(access_token, realm, character_name):
    url = f"https://eu.api.blizzard.com/profile/wow/character/{realm}/{character_name}?namespace=profile-eu&locale=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()

def get_talent_data(access_token, realm, character_name):
    url = f"https://eu.api.blizzard.com/profile/wow/character/{realm}/{character_name}/talents?namespace=profile-eu&locale=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()

def get_equipment_data(access_token, equipment_url):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(equipment_url, headers=headers)
    return response.json()

def get_stats_data(access_token, stats_url):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(stats_url, headers=headers)
    return response.json()

def get_talent_data(access_token, realm, character_name):
    url = f"https://eu.api.blizzard.com/profile/wow/character/{realm}/{character_name}/specializations?namespace=profile-eu&locale=en_GB&access_token={access_token}"
    response = requests.get(url)
    return response.json()

