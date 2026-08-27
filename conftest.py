import pytest
from api_client import APIClient
from helpers import (
    generate_user_data,
    create_user,
    delete_user,
    get_ingredients_from_server
)


@pytest.fixture
def api_client():
    """Возвращает экземпляр APIClient"""
    return APIClient()


@pytest.fixture
def authorized_user(api_client):
    """
    Создает авторизованного пользователя и возвращает его токен и данные.
    Это предусловие для тестов — регистрация НЕ проверяется здесь.
    """
    user_data = generate_user_data()
    response, _ = create_user(api_client, user_data)
    
    token = response.json().get("accessToken") if response.status_code == 200 else None
    
    yield {
        "user_data": user_data,
        "token": token
    }
    
    # Очистка после теста
    if token:
        delete_user(api_client, token)


@pytest.fixture
def ingredients(api_client):
    """Возвращает реальные ингредиенты с сервера"""
    return get_ingredients_from_server(api_client)