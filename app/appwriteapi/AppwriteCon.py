from appwrite.client import Client
from appwrite.services.database import Database

class AppwriteService:
    def __init__(self, url: str, apikey: str):
        self.url = url
        self.apikey = apikey
        self.client = self.connect(url, apikey)

    def connect(self, url:str, apikey:str):
        client = Client()
        client.set_endpoint(url)
        client.set_self_signed(True)
        client.set_key(apikey)
        return client


