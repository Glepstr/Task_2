import requests
from data import BASE_URL


class APIClient:
    """Клиент для работы с API Stellar Burgers"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()

    def post(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=data, headers=headers)

    def patch(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.patch(url, json=data, headers=headers)

    def get(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, headers=headers)

    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url, headers=headers)