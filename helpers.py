import random
import string
from data import VALID_INGREDIENTS

def generate_random_string(length=8):
    """Генерирует случайную строку из букв и цифр"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data():
    """Генерирует уникальные данные для пользователя"""
    email = f"test_{generate_random_string(10)}@yandex.ru"
    password = generate_random_string(10)
    name = f"User_{generate_random_string(6)}"
    return {
        "email": email,
        "password": password,
        "name": name
    }

def get_ingredients_list():
    """Возвращает список валидных ингредиентов"""
    return VALID_INGREDIENTS