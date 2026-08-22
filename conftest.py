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
def created_user(api_client):
    """
    Создает пользователя в системе и возвращает его данные с токенами.
    После теста удаляет пользователя (даже если тест упал).
    """
    # Создаем пользователя
    response, user_data = create_user(api_client)
    
    # Сохраняем response для проверок в тесте
    user_data["_registration_response"] = response
    user_data["_access_token"] = response.json().get("accessToken") if response.status_code == 200 else None
    
    yield user_data
    
    # Постусловие: удаляем пользователя после теста
    if user_data.get("_access_token"):
        delete_user(api_client, user_data["_access_token"])


@pytest.fixture
def ingredients(api_client):
    """Возвращает реальные ингредиенты с сервера"""
    return get_ingredients_from_server(api_client)