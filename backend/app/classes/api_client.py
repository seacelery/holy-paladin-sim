import requests
from .config import CLIENT_ID, CLIENT_SECRET
from functools import cache

class APIClient:
    _instance = None
    api_call_count = 0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClient, cls).__new__(cls)
            cls._instance.access_token = cls._get_access_token()
        return cls._instance

    @staticmethod
    def _get_access_token():
        url = "https://eu.battle.net/oauth/token"
        APIClient.api_call_count += 1
        response = requests.post(url, data={'grant_type': 'client_credentials'}, auth=(CLIENT_ID, CLIENT_SECRET))
        return response.json()["access_token"]

    @cache
    def get_item_media(self, url_start):
        url = f"{url_start}&locale=en_GB&access_token={self.access_token}"
        response = requests.get(url)
        return response.json()