import allure
from data import MSG_UNAUTHORIZED
from helpers import get_user_orders


@allure.epic("Заказы")
class TestOrdersList:
    
    @allure.feature("Получение заказов пользователя")
    @allure.story("Авторизованный пользователь")
    def test_get_user_orders_authorized(self, api_client, authorized_user):
        """
        Получение заказов пользователя с авторизацией.
        Предусловие: авторизованный пользователь (фикстура authorized_user)
        """
        assert authorized_user["_registration_response"].status_code == 200
        assert authorized_user["token"] is not None
        
        token = authorized_user["token"]
        
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
        # Очистка выполняется в фикстуре authorized_user
    
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