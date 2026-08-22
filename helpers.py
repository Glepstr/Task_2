import random
import string
from data import (
    AUTH_REGISTER_ENDPOINT, AUTH_LOGIN_ENDPOINT,
    AUTH_USER_ENDPOINT, ORDERS_ENDPOINT, INGREDIENTS_ENDPOINT
)


def generate_random_string(length=8):
    """Генерирует случайную строку из букв и цифр"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_user_data():
    """Генерирует уникальные данные для пользователя"""
    email = f"test_{generate_random_string(10)}@yandex.ru"
    password = generate_random_string(10)
    name = f"User_{generate_random_string(6)}"
    return {
        "email": email,
        "password": password,
        "name": name
    }


def create_user(api_client, user_data=None):
    """
    Создает пользователя в системе.
    Если user_data не передан, генерирует новые данные.
    Возвращает tuple: (response, user_data)
    """
    if user_data is None:
        user_data = generate_user_data()
    
    response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
    return response, user_data


def delete_user(api_client, access_token):
    """Удаляет пользователя по токену"""
    if access_token:
        headers = {"Authorization": access_token}
        try:
            return api_client.delete(AUTH_USER_ENDPOINT, headers=headers)
        except Exception:
            pass
    return None


def login_user(api_client, email, password):
    """Выполняет логин пользователя"""
    login_data = {"email": email, "password": password}
    return api_client.post(AUTH_LOGIN_ENDPOINT, data=login_data)


def update_user(api_client, access_token, update_data):
    """Обновляет данные пользователя"""
    headers = {"Authorization": access_token} if access_token else None
    return api_client.patch(AUTH_USER_ENDPOINT, data=update_data, headers=headers)


def get_user_orders(api_client, access_token):
    """Получает заказы пользователя"""
    headers = {"Authorization": access_token} if access_token else None
    return api_client.get(ORDERS_ENDPOINT, headers=headers)


def create_order(api_client, ingredients, access_token=None):
    """Создает заказ. Если access_token передан - с авторизацией, иначе без"""
    order_data = {"ingredients": ingredients}
    headers = {"Authorization": access_token} if access_token else None
    return api_client.post(ORDERS_ENDPOINT, data=order_data, headers=headers)


def get_ingredients_from_server(api_client):
    """Получает список ингредиентов с сервера"""
    response = api_client.get(INGREDIENTS_ENDPOINT)
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("data"):
            ingredients = [item["_id"] for item in data["data"][:2]]
            if ingredients:
                return ingredients
    return []