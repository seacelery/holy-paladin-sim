import requests

def get_access_token(client_id, client_secret):
    url = "https://eu.battle.net/oauth/token"
    response = requests.post(url, data={'grant_type': 'client_credentials'}, auth=(client_id, client_secret))
    return response.json()["access_token"]

def get_spell_icon_data(access_token, spellId):
    url = f'https://eu.api.blizzard.com/data/wow/media/spell/{spellId}?locale=en_GB&access_token={access_token}&namespace=static-eu'
    response = requests.get(url)
    return response.json()

client_id = "57cdb961fae04b8f9dc4d3caea3716db"
client_secret = "rIIdFk2In9dQfBUxbPmH6ee4DDDO6oUV"
access_token = get_access_token(client_id, client_secret)

icon = get_spell_icon_data(access_token, 156910)
print(icon)