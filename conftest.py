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
    """Генерирует уникальные данные пользователя"""
    return generate_user_data()


@pytest.fixture
def created_user(api_client):
    """
    Создает пользователя в системе и возвращает его данные с токенами.
    Если создание не удалось, фикстура вернет response с ошибкой,
    и тест сам обработает эту ситуацию.
    """
    user_data = generate_user_data()
    
    response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
    
    # Сохраняем response в данных, чтобы тест мог проверить статус
    user_data["_registration_response"] = response
    
    if response.status_code == 200:
        json_data = response.json()
        user_data["accessToken"] = json_data.get("accessToken")
        user_data["refreshToken"] = json_data.get("refreshToken")
    else:
        # Если регистрация не удалась, токенов нет
        user_data["accessToken"] = None
        user_data["refreshToken"] = None
    
    yield user_data
    
    # Удаление пользователя после теста (только если создание было успешным)
    if user_data.get("accessToken"):
        try:
            headers = {"Authorization": user_data["accessToken"]}
            api_client.delete(AUTH_USER_ENDPOINT, headers=headers)
        except Exception:
            pass  # Игнорируем ошибки при удалении


@pytest.fixture
def authorized_headers(created_user):
    """
    Возвращает заголовки с авторизационным токеном.
    Если токена нет, вернет пустой словарь.
    """
    if created_user.get("accessToken"):
        return {"Authorization": created_user["accessToken"]}
    return {}


@pytest.fixture
def ingredients(api_client):
    """
    Возвращает реальные ингредиенты с сервера.
    Фикстура НЕ содержит assert.
    """
    response = api_client.get(INGREDIENTS_ENDPOINT)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("data"):
            ingredients = [item["_id"] for item in data["data"][:2]]
            if ingredients:
                return ingredients
    
    # fallback: возвращаем список, который точно вызовет ошибку, если что-то пошло не так
    return []