import allure
from data import ORDERS_ENDPOINT, MSG_UNAUTHORIZED

@allure.epic("Заказы")
class TestOrdersList:
    
    @allure.feature("Получение заказов пользователя")
    @allure.story("Авторизованный пользователь")
    def test_get_user_orders_authorized(self, api_client, authorized_headers):
        """Получение заказов конкретного пользователя с авторизацией"""
        with allure.step("Отправить запрос на получение заказов пользователя"):
            response = api_client.get(ORDERS_ENDPOINT, headers=authorized_headers)
        
        with allure.step("Проверить код ответа 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "orders" in json_data
            assert "total" in json_data
            assert "totalToday" in json_data
            assert isinstance(json_data["orders"], list)
    
    @allure.feature("Получение заказов пользователя")
    @allure.story("Неавторизованный пользователь")
    def test_get_user_orders_unauthorized(self, api_client):
        """Получение заказов пользователя без авторизации"""
        with allure.step("Отправить запрос на получение заказов пользователя без авторизации"):
            response = api_client.get(ORDERS_ENDPOINT)
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_UNAUTHORIZED