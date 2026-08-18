import allure
import pytest
from data import (
    AUTH_REGISTER_ENDPOINT, AUTH_LOGIN_ENDPOINT, AUTH_USER_ENDPOINT,
    MSG_USER_ALREADY_EXISTS, MSG_REQUIRED_FIELDS,
    MSG_INCORRECT_CREDENTIALS, MSG_UNAUTHORIZED, MSG_EMAIL_ALREADY_EXISTS
)
from helpers import generate_user_data, generate_random_string

@allure.epic("Пользователь")
class TestUser:
    
    @allure.feature("Создание пользователя")
    @allure.story("Успешное создание")
    def test_create_user_success(self, api_client):
        """Создание уникального пользователя - успешный сценарий"""
        user_data = generate_user_data()
        
        with allure.step("Отправить запрос на регистрацию"):
            response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
        
        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200
            assert response.json()["success"] is True
        
        with allure.step("Проверить структуру ответа"):
            json_data = response.json()
            assert "accessToken" in json_data
            assert "refreshToken" in json_data
            assert json_data["user"]["email"] == user_data["email"]
            assert json_data["user"]["name"] == user_data["name"]
        
        # Удаление созданного пользователя
        headers = {"Authorization": json_data["accessToken"]}
        api_client.delete(AUTH_USER_ENDPOINT, headers=headers)
    
    @allure.feature("Создание пользователя")
    @allure.story("Ошибки при создании")
    def test_create_user_already_exists(self, api_client, created_user):
        """Создание пользователя, который уже зарегистрирован"""
        user_data = {
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"]
        }
        
        with allure.step("Отправить запрос на регистрацию существующего пользователя"):
            response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_USER_ALREADY_EXISTS
    
    @allure.feature("Создание пользователя")
    @allure.story("Ошибки при создании")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, api_client, missing_field):
        """Создание пользователя без одного из обязательных полей"""
        user_data = generate_user_data()
        del user_data[missing_field]
        
        with allure.step(f"Отправить запрос на регистрацию без поля '{missing_field}'"):
            response = api_client.post(AUTH_REGISTER_ENDPOINT, data=user_data)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_REQUIRED_FIELDS
    
    @allure.feature("Логин пользователя")
    @allure.story("Успешный вход")
    def test_login_success(self, api_client, created_user):
        """Логин под существующим пользователем"""
        login_data = {
            "email": created_user["email"],
            "password": created_user["password"]
        }
        
        with allure.step("Отправить запрос на логин"):
            response = api_client.post(AUTH_LOGIN_ENDPOINT, data=login_data)
        
        with allure.step("Проверить код ответа 200 и структуру ответа"):
            assert response.status_code == 200
            json_data = response.json()
            assert json_data["success"] is True
            assert "accessToken" in json_data
            assert "refreshToken" in json_data
            assert json_data["user"]["email"] == created_user["email"]
            assert json_data["user"]["name"] == created_user["name"]
    
    @allure.feature("Логин пользователя")
    @allure.story("Ошибки при входе")
    @pytest.mark.parametrize("email,password", [
        ("wrong@yandex.ru", "password123"),
        ("test@yandex.ru", "wrongpassword"),
        ("wrong@yandex.ru", "wrongpassword")
    ])
    def test_login_invalid_credentials(self, api_client, email, password):
        """Логин с неверным логином и паролем"""
        login_data = {
            "email": email,
            "password": password
        }
        
        with allure.step("Отправить запрос на логин с неверными данными"):
            response = api_client.post(AUTH_LOGIN_ENDPOINT, data=login_data)
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_INCORRECT_CREDENTIALS
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Авторизованный пользователь")
    @pytest.mark.parametrize("field,new_value", [
        ("email", None),  # Будет сгенерирован уникальный email
        ("password", "new_password_123"),
        ("name", "NewUserName")
    ])
    def test_update_user_authorized(self, api_client, created_user, authorized_headers, field, new_value):
        """Изменение данных пользователя с авторизацией"""
        # Если поле email, генерируем уникальный email
        if field == "email" and new_value is None:
            new_value = f"new_{generate_random_string(8)}@yandex.ru"
        
        update_data = {field: new_value}
        
        with allure.step(f"Отправить запрос на изменение поля '{field}'"):
            response = api_client.patch(AUTH_USER_ENDPOINT, data=update_data, headers=authorized_headers)
        
        with allure.step("Проверить код ответа 200 и обновленные данные"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}. Тело: {response.text}"
            json_data = response.json()
            assert json_data["success"] is True
            
            # Для пароля проверяем через логин, так как сервер не возвращает пароль
            if field == "password":
                login_data = {
                    "email": created_user["email"],
                    "password": new_value
                }
                login_response = api_client.post(AUTH_LOGIN_ENDPOINT, data=login_data)
                assert login_response.status_code == 200, "Не удалось войти с новым паролем"
            else:
                # Для email и name проверяем прямо в ответе
                assert json_data["user"][field] == new_value
        
        # Проверяем, что остальные поля не изменились
        if field != "email":
            assert json_data["user"]["email"] == created_user["email"]
        if field != "name":
            assert json_data["user"]["name"] == created_user["name"]
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Неавторизованный пользователь")
    @pytest.mark.parametrize("field,new_value", [
        ("email", "new_email@yandex.ru"),
        ("password", "new_password_123"),
        ("name", "NewUserName")
    ])
    def test_update_user_unauthorized(self, api_client, field, new_value):
        """Изменение данных пользователя без авторизации"""
        update_data = {field: new_value}
        
        with allure.step(f"Отправить запрос на изменение поля '{field}' без авторизации"):
            response = api_client.patch(AUTH_USER_ENDPOINT, data=update_data)
        
        with allure.step("Проверить код ответа 401 и сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_UNAUTHORIZED
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Ошибки при изменении")
    def test_update_user_email_already_exists(self, api_client, created_user, authorized_headers):
        """Попытка изменить email на уже существующий"""
        # Создаем второго пользователя
        other_user_data = generate_user_data()
        other_response = api_client.post(AUTH_REGISTER_ENDPOINT, data=other_user_data)
        assert other_response.status_code == 200
        
        update_data = {"email": other_user_data["email"]}
        
        with allure.step("Отправить запрос на изменение email на уже существующий"):
            response = api_client.patch(AUTH_USER_ENDPOINT, data=update_data, headers=authorized_headers)
        
        with allure.step("Проверить код ответа 403 и сообщение об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == MSG_EMAIL_ALREADY_EXISTS
        
        # Удаляем второго пользователя
        other_headers = {"Authorization": other_response.json()["accessToken"]}
        api_client.delete(AUTH_USER_ENDPOINT, headers=other_headers)
    
    @allure.feature("Изменение данных пользователя")
    @allure.story("Ошибки при изменении")
    def test_update_user_unauthorized_error_message(self, api_client):
        """Проверка сообщения об ошибке для неавторизованного пользователя"""
        update_data = {"name": "NewName"}
        
        with allure.step("Отправить запрос на изменение данных без авторизации"):
            response = api_client.patch(AUTH_USER_ENDPOINT, data=update_data)
        
        with allure.step("Проверить сообщение об ошибке"):
            assert response.status_code == 401
            assert response.json()["message"] == MSG_UNAUTHORIZED