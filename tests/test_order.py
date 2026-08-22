import allure
import pytest
from data import (
    ORDERS_ENDPOINT, MSG_INGREDIENTS_REQUIRED,
    INVALID_INGREDIENT_HASH
)
from helpers import generate_user_data


@allure.epic("Заказы")
class TestOrder:
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_with_ingredients(self, api_client, ingredients):
        """Создание заказа с ингредиентами авторизованным пользователем"""
        # Создаем пользователя для теста
        user_data = generate_user_data()
        register_response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
        assert register_response.status_code == 200, "Не удалось создать пользователя"
        token = register_response.json().get("accessToken")
        
        # Проверяем, что есть ингредиенты для заказа
        assert len(ingredients) > 0, "Нет доступных ингредиентов"
        
        order_data = {"ingredients": ingredients}
        headers = {"Authorization": token}
        
        with allure.step("Отправить запрос на создание заказа"):
            response = api_client.post(ORDERS_ENDPOINT, data=order_data, headers=headers)
        
        with allure.step("Проверить код ответа 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "name" in json_data
            assert "order" in json_data
            assert "number" in json_data["order"]
        
        # Удаляем пользователя
        if token:
            api_client.delete(AUTH_USER_ENDPOINT, headers={"Authorization": token})
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_without_ingredients(self, api_client):
        """Создание заказа без ингредиентов авторизованным пользователем"""
        # Создаем пользователя для теста
        user_data = generate_user_data()
        register_response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
        assert register_response.status_code == 200, "Не удалось создать пользователя"
        token = register_response.json().get("accessToken")
        
        order_data = {"ingredients": []}
        headers = {"Authorization": token}
        
        with allure.step("Отправить запрос на создание заказа без ингредиентов"):
            response = api_client.post(ORDERS_ENDPOINT, data=order_data, headers=headers)
        
        with allure.step("Проверить код ответа 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INGREDIENTS_REQUIRED
        
        # Удаляем пользователя
        if token:
            api_client.delete(AUTH_USER_ENDPOINT, headers={"Authorization": token})
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_invalid_hash(self, api_client):
        """Создание заказа с неверным хешем ингредиентов авторизованным пользователем"""
        # Создаем пользователя для теста
        user_data = generate_user_data()
        register_response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
        assert register_response.status_code == 200, "Не удалось создать пользователя"
        token = register_response.json().get("accessToken")
        
        order_data = {"ingredients": [INVALID_INGREDIENT_HASH]}
        headers = {"Authorization": token}
        
        with allure.step("Отправить запрос на создание заказа с неверным хешем"):
            response = api_client.post(ORDERS_ENDPOINT, data=order_data, headers=headers)
        
        with allure.step("Проверить код ответа 500"):
            assert response.status_code == 500
        
        # Удаляем пользователя
        if token:
            api_client.delete(AUTH_USER_ENDPOINT, headers={"Authorization": token})
    
    @allure.feature("Создание заказа")
    @allure.story("Неавторизованный пользователь")
    def test_create_order_unauthorized_with_ingredients(self, api_client, ingredients):
        """Создание заказа с ингредиентами неавторизованным пользователем"""
        # Проверяем, что есть ингредиенты для заказа
        assert len(ingredients) > 0, "Нет доступных ингредиентов"
        
        order_data = {"ingredients": ingredients}
        
        with allure.step("Отправить запрос на создание заказа без авторизации"):
            response = api_client.post(ORDERS_ENDPOINT, data=order_data)
        
        with allure.step("Проверить код ответа 200 (создание заказа доступно без авторизации)"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "order" in json_data
    
    @allure.feature("Создание заказа")
    @allure.story("Неавторизованный пользователь")
    def test_create_order_unauthorized_without_ingredients(self, api_client):
        """Создание заказа без ингредиентов неавторизованным пользователем"""
        order_data = {"ingredients": []}
        
        with allure.step("Отправить запрос на создание заказа без ингредиентов без авторизации"):
            response = api_client.post(ORDERS_ENDPOINT, data=order_data)
        
        with allure.step("Проверить код ответа 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INGREDIENTS_REQUIRED