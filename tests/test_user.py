import allure
from data import (
    MSG_USER_ALREADY_EXISTS, MSG_REQUIRED_FIELDS,
    MSG_INCORRECT_CREDENTIALS, MSG_UNAUTHORIZED, MSG_EMAIL_ALREADY_EXISTS
)
from helpers import (
    generate_user_data,
    create_user,
    delete_user,
    login_user,
    update_user,
    generate_random_string
)


@allure.epic("Пользователь")
class TestUser:
    
    @allure.feature("Создание пользователя")
    @allure.story("Успешное создание")
    def test_create_user_success(self, api_client):
        """Создание уникального пользователя - успешный сценарий"""
        user_data = generate_user_data()
        
        with allure.step("Отправить запрос на регистрацию"):
            response, _ = create_user(api_client, user_data)
        
        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
            assert response.json()["success"] is True
        
        with allure.step("Проверить структуру ответа"):
            json_data = response.json()
            assert "accessToken" in json_data
            assert "refreshToken" in json_data
            assert json_data["user"]["email"] == user_data["email"]
            assert json_data["user"]["name"] == user_data["name"]
        
        # Очистка после теста
        token = response.json().get("accessToken")
        delete_user(api_client, token)
    
    @allure.feature("Создание пользователя")
    @allure.story("Ошибки при создании")
    def test_create_user_already_exists(self, api_client, authorized_user):
        """
        Создание пользователя, который уже зарегистрирован.
        Предусловие: существующий пользователь (фикстура authorized_user)
        """
        # Берем данные существующего пользователя из фикстуры
        existing_user_data = authorized_user["user_data"]
        
        with allure.step("Отправить запрос на регистрацию существующего пользователя"):
            response, _ = create_user(api_client, existing_user_data)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_USER_ALREADY_EXISTS
        # Очистка выполняется в фикстуре authorized_user
    
    @allure.feature("Создание пользователя")
    @allure.story("Ошибки при создании")
    def test_create_user_missing_email(self, api_client):
        """Создание пользователя без email"""
        user_data = generate_user_data()
        del user_data["email"]
        
        with allure.step("Отправить запрос на регистрацию без email"):
            response, _ = create_user(api_client, user_data)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_REQUIRED_FIELDS
    
    @allure.feature("Создание пользователя")
    @allure.story("Ошибки при создании")
    def test_create_user_missing_password(self, api_client):
        """Создание пользователя без password"""
        user_data = generate_user_data()
        del user_data["password"]
        
        with allure.step("Отправить запрос на регистрацию без password"):
            response, _ = create_user(api_client, user_data)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_REQUIRED_FIELDS
    
    @allure.feature("Создание пользователя")
    @allure.story("Ошибки при создании")
    def test_create_user_missing_name(self, api_client):
        """Создание пользователя без name"""
        user_data = generate_user_data()
        del user_data["name"]
        
        with allure.step("Отправить запрос на регистрацию без name"):
            response, _ = create_user(api_client, user_data)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_REQUIRED_FIELDS
    
    @allure.feature("Логин пользователя")
    @allure.story("Успешный вход")
    def test_login_success(self, api_client, authorized_user):
        """
        Логин под существующим пользователем.
        Предусловие: существующий пользователь (фикстура authorized_user)
        """
        user_data = authorized_user["user_data"]
        
        with allure.step("Отправить запрос на логин"):
            response = login_user(api_client, user_data["email"], user_data["password"])
        
        with allure.step("Проверить код ответа 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "accessToken" in json_data
            assert "refreshToken" in json_data
            assert json_data["user"]["email"] == user_data["email"]
            assert json_data["user"]["name"] == user_data["name"]
        # Очистка выполняется в фикстуре authorized_user
    
    @allure.feature("Логин пользователя")
    @allure.story("Ошибки при входе")
    def test_login_invalid_email(self, api_client):
        """Логин с неверным email"""
        with allure.step("Отправить запрос на логин с неверным email"):
            response = login_user(api_client, "wrong@yandex.ru", "password123")
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INCORRECT_CREDENTIALS
    
    @allure.feature("Логин пользователя")
    @allure.story("Ошибки при входе")
    def test_login_invalid_password(self, api_client, authorized_user):
        """
        Логин с неверным паролем.
        Предусловие: существующий пользователь (фикстура authorized_user)
        """
        user_data = authorized_user["user_data"]
        
        with allure.step("Отправить запрос на логин с неверным паролем"):
            response = login_user(api_client, user_data["email"], "wrongpassword")
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INCORRECT_CREDENTIALS
        # Очистка выполняется в фикстуре authorized_user
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Авторизованный пользователь")
    def test_update_user_email_authorized(self, api_client, authorized_user):
        """
        Изменение email авторизованным пользователем.
        Предусловие: авторизованный пользователь (фикстура authorized_user)
        """
        token = authorized_user["token"]
        new_email = f"new_{generate_random_string(8)}@yandex.ru"
        update_data = {"email": new_email}
        
        with allure.step("Отправить запрос на изменение email"):
            response = update_user(api_client, token, update_data)
        
        with allure.step("Проверить код ответа 200 и обновленный email"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert json_data["user"]["email"] == new_email
        # Очистка выполняется в фикстуре authorized_user
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Авторизованный пользователь")
    def test_update_user_password_authorized(self, api_client, authorized_user):
        """
        Изменение пароля авторизованным пользователем.
        Предусловие: авторизованный пользователь (фикстура authorized_user)
        """
        token = authorized_user["token"]
        user_data = authorized_user["user_data"]
        new_password = "new_password_123"
        update_data = {"password": new_password}
        
        with allure.step("Отправить запрос на изменение пароля"):
            response = update_user(api_client, token, update_data)
        
        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
            assert response.json()["success"] is True
        
        with allure.step("Проверить, что новый пароль работает"):
            login_response = login_user(api_client, user_data["email"], new_password)
            assert login_response.status_code == 200
        # Очистка выполняется в фикстуре authorized_user
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Авторизованный пользователь")
    def test_update_user_name_authorized(self, api_client, authorized_user):
        """
        Изменение имени авторизованным пользователем.
        Предусловие: авторизованный пользователь (фикстура authorized_user)
        """
        token = authorized_user["token"]
        new_name = "NewUserName"
        update_data = {"name": new_name}
        
        with allure.step("Отправить запрос на изменение имени"):
            response = update_user(api_client, token, update_data)
        
        with allure.step("Проверить код ответа 200 и обновленное имя"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert json_data["user"]["name"] == new_name
        # Очистка выполняется в фикстуре authorized_user
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Неавторизованный пользователь")
    def test_update_user_email_unauthorized(self, api_client):
        """Изменение email без авторизации"""
        update_data = {"email": "new_email@yandex.ru"}
        
        with allure.step("Отправить запрос на изменение email без авторизации"):
            response = update_user(api_client, None, update_data)
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_UNAUTHORIZED
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Неавторизованный пользователь")
    def test_update_user_password_unauthorized(self, api_client):
        """Изменение пароля без авторизации"""
        update_data = {"password": "new_password_123"}
        
        with allure.step("Отправить запрос на изменение пароля без авторизации"):
            response = update_user(api_client, None, update_data)
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_UNAUTHORIZED
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Неавторизованный пользователь")
    def test_update_user_name_unauthorized(self, api_client):
        """Изменение имени без авторизации"""
        update_data = {"name": "NewUserName"}
        
        with allure.step("Отправить запрос на изменение имени без авторизации"):
            response = update_user(api_client, None, update_data)
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_UNAUTHORIZED
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Ошибки при изменении")
    def test_update_user_email_already_exists(self, api_client, authorized_user):
        """
        Попытка изменить email на уже существующий.
        Предусловие: два пользователя (один из фикстуры, второй создается в тесте)
        """
        # Первый пользователь из фикстуры
        token1 = authorized_user["token"]
        user2_data = generate_user_data()
        
        # Создаем второго пользователя
        response2, _ = create_user(api_client, user2_data)
        assert response2.status_code == 200
        token2 = response2.json().get("accessToken")
        
        with allure.step("Отправить запрос на изменение email на уже существующий"):
            update_data = {"email": user2_data["email"]}
            response = update_user(api_client, token1, update_data)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_EMAIL_ALREADY_EXISTS
        
        # Очистка: удаляем второго пользователя (первый удалится в фикстуре)
        delete_user(api_client, token2)