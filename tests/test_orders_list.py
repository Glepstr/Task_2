import allure
from data import MSG_UNAUTHORIZED
from helpers import (
    generate_user_data,
    create_user,
    delete_user,
    get_user_orders
)


@allure.epic("Заказы")
class TestOrdersList:
    
    @allure.feature("Получение заказов пользователя")
    @allure.story("Авторизованный пользователь")
    def test_get_user_orders_authorized(self, api_client):
        """Получение заказов пользователя с авторизацией"""
        user_data = generate_user_data()
        register_response, _ = create_user(api_client, user_data)
        assert register_response.status_code == 200
        token = register_response.json().get("accessToken")
        
        with allure.step("Отправить запрос на получение заказов пользователя"):
            response = get_user_orders(api_client, token)
        
        with allure.step("Проверить код ответа 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "orders" in json_data
            assert "total" in json_data
            assert "totalToday" in json_data
            assert isinstance(json_data["orders"], list)
        
        delete_user(api_client, token)
    
    @allure.feature("Получение заказов пользователя")
    @allure.story("Неавторизованный пользователь")
    def test_get_user_orders_unauthorized(self, api_client):
        """Получение заказов пользователя без авторизации"""
        with allure.step("Отправить запрос на получение заказов без авторизации"):
            response = get_user_orders(api_client, None)
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_UNAUTHORIZED