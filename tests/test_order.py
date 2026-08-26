import allure
from data import MSG_INGREDIENTS_REQUIRED, INVALID_INGREDIENT_HASH
from helpers import create_order


@allure.epic("Заказы")
class TestOrder:
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_with_ingredients(self, api_client, authorized_user, ingredients):
        """
        Создание заказа с ингредиентами авторизованным пользователем.
        Предусловие: авторизованный пользователь (фикстура authorized_user)
        """
        # Проверяем, что пользователь создан успешно
        assert authorized_user["_registration_response"].status_code == 200
        assert authorized_user["token"] is not None
        
        token = authorized_user["token"]
        
        with allure.step("Отправить запрос на создание заказа"):
            response = create_order(api_client, ingredients, token)
        
        with allure.step("Проверить код ответа 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "name" in json_data
            assert "order" in json_data
            assert "number" in json_data["order"]
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_without_ingredients(self, api_client, authorized_user):
        """
        Создание заказа без ингредиентов авторизованным пользователем.
        Предусловие: авторизованный пользователь (фикстура authorized_user)
        """
        assert authorized_user["_registration_response"].status_code == 200
        assert authorized_user["token"] is not None
        
        token = authorized_user["token"]
        
        with allure.step("Отправить запрос на создание заказа без ингредиентов"):
            response = create_order(api_client, [], token)
        
        with allure.step("Проверить код ответа 400 и сообщение об ошибке"):
            assert response.status_code == 400
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INGREDIENTS_REQUIRED
    
    @allure.feature("Создание заказа")
    @allure.story("Авторизованный пользователь")
    def test_create_order_authorized_invalid_hash(self, api_client, authorized_user):
        """
        Создание заказа с неверным хешем ингредиентов.
        Предусловие: авторизованный пользователь (фикстура authorized_user)
        """
        assert authorized_user["_registration_response"].status_code == 200
        assert authorized_user["token"] is not None
        
        token = authorized_user["token"]
        
        with allure.step("Отправить запрос на создание заказа с неверным хешем"):
            response = create_order(api_client, [INVALID_INGREDIENT_HASH], token)
        
        with allure.step("Проверить код ответа 500"):
            assert response.status_code == 500
    
    @allure.feature("Создание заказа")
    @allure.story("Неавторизованный пользователь")
    def test_create_order_unauthorized_with_ingredients(self, api_client, ingredients):
        """Создание заказа с ингредиентами неавторизованным пользователем"""
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