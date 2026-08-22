import allure
from data import MSG_INGREDIENTS_REQUIRED, INVALID_INGREDIENT_HASH
from helpers import (
    generate_user_data,
    create_user,
    delete_user,
    create_order,
    login_user
)


@allure.epic("Заказы")
class TestOrder:
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_with_ingredients(self, api_client, ingredients):
        """Создание заказа с ингредиентами авторизованным пользователем"""
        user_data = generate_user_data()
        register_response, _ = create_user(api_client, user_data)
        assert register_response.status_code == 200
        token = register_response.json().get("accessToken")
        assert len(ingredients) > 0, "Нет доступных ингредиентов"
        
        with allure.step("Отправить запрос на создание заказа"):
            response = create_order(api_client, ingredients, token)
        
        with allure.step("Проверить код ответа 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "name" in json_data
            assert "order" in json_data
            assert "number" in json_data["order"]
        
        delete_user(api_client, token)
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_without_ingredients(self, api_client):
        """Создание заказа без ингредиентов авторизованным пользователем"""
        user_data = generate_user_data()
        register_response, _ = create_user(api_client, user_data)
        assert register_response.status_code == 200
        token = register_response.json().get("accessToken")
        
        with allure.step("Отправить запрос на создание заказа без ингредиентов"):
            response = create_order(api_client, [], token)
        
        with allure.step("Проверить код ответа 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INGREDIENTS_REQUIRED
        
        delete_user(api_client, token)
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_invalid_hash(self, api_client):
        """Создание заказа с неверным хешем ингредиентов"""
        user_data = generate_user_data()
        register_response, _ = create_user(api_client, user_data)
        assert register_response.status_code == 200
        token = register_response.json().get("accessToken")
        
        with allure.step("Отправить запрос на создание заказа с неверным хешем"):
            response = create_order(api_client, [INVALID_INGREDIENT_HASH], token)
        
        with allure.step("Проверить код ответа 500"):
            assert response.status_code == 500
        
        delete_user(api_client, token)
    
    @allure.feature("Создание заказа")
    @allure.story("Неавторизованный пользователь")
    def test_create_order_unauthorized_with_ingredients(self, api_client, ingredients):
        """Создание заказа с ингредиентами неавторизованным пользователем"""
        assert len(ingredients) > 0, "Нет доступных ингредиентов"
        
        with allure.step("Отправить запрос на создание заказа без авторизации"):
            response = create_order(api_client, ingredients)
        
        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "order" in json_data
    
    @allure.feature("Создание заказа")
    @allure.story("Неавторизованный пользователь")
    def test_create_order_unauthorized_without_ingredients(self, api_client):
        """Создание заказа без ингредиентов неавторизованным пользователем"""
        with allure.step("Отправить запрос на создание заказа без ингредиентов без авторизации"):
            response = create_order(api_client, [])
        
        with allure.step("Проверить код ответа 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INGREDIENTS_REQUIRED