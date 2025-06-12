import os
import requests
from dotenv import load_dotenv

class BuiltWithClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('BUILTWITH_API_KEY')
        self.base_url = 'https://api.builtwith.com/v19/api.json'

    def get_website_data(self, domain):
        params = {
            'KEY': self.api_key,
            'LOOKUP': domain
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

    def save_to_json(self, data, filename):
        import json
        with open(f'data/{filename}', 'w') as f:
            json.dump(data, f, indent=4)