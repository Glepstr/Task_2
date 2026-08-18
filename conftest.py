import pytest
import requests
from data import (
    BASE_URL, AUTH_REGISTER_ENDPOINT, AUTH_LOGIN_ENDPOINT,
    AUTH_USER_ENDPOINT, ORDERS_ENDPOINT, INGREDIENTS_ENDPOINT
)
from helpers import generate_user_data

@pytest.fixture
def api_client():
    """Базовый клиент для API запросов"""
    class APIClient:
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

    return APIClient()

@pytest.fixture
def test_user_data():
    """Создает уникальные данные пользователя и удаляет его после теста"""
    user_data = generate_user_data()
    yield user_data

@pytest.fixture
def created_user(api_client):
    """Создает пользователя в системе и возвращает его данные с токенами"""
    user_data = generate_user_data()
    
    response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
    
    user_data["accessToken"] = response.json().get("accessToken")
    user_data["refreshToken"] = response.json().get("refreshToken")
    
    yield user_data
    
    # Удаление пользователя после теста
    if "accessToken" in user_data and user_data["accessToken"]:
        headers = {"Authorization": user_data["accessToken"]}
        api_client.delete(AUTH_USER_ENDPOINT, headers=headers)

@pytest.fixture
def authorized_headers(created_user):
    """Возвращает заголовки с авторизационным токеном"""
    return {"Authorization": created_user["accessToken"]}

@pytest.fixture
def ingredients(api_client):
    """Возвращает реальные ингредиенты с сервера"""
    response = api_client.get(INGREDIENTS_ENDPOINT)
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("data"):
            # Берем первые два ингредиента
            ingredients = [item["_id"] for item in data["data"][:2]]
            if ingredients:
                return ingredients
    
    # Если не удалось получить ингредиенты, используем запасные
    return [
        "60d3b41abdacab0026a733c6",  # Булка
        "60d3b41abdacab0026a733c7"   # Соус
    ]