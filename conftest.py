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
def test_user_data():
    """
    Возвращает сгенерированные данные пользователя.
    Используем return, так как нет cleanup после теста.
    """
    return generate_user_data()


@pytest.fixture
def authorized_user(api_client):
    """
    Создает авторизованного пользователя и возвращает его токен и данные.
    Используется в тестах, где требуется авторизованный пользователь как предусловие.
    """
    user_data = generate_user_data()
    response, _ = create_user(api_client, user_data)
    
    # Гарантируем, что пользователь создан (это предусловие)
    assert response.status_code == 200, "Не удалось создать пользователя для теста"
    
    token = response.json().get("accessToken")
    
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