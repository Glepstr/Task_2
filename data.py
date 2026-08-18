BASE_URL = "https://stellarburgers.education-services.ru"

# Эндпоинты
INGREDIENTS_ENDPOINT = "/api/ingredients"
ORDERS_ENDPOINT = "/api/orders"
AUTH_REGISTER_ENDPOINT = "/api/auth/register"
AUTH_LOGIN_ENDPOINT = "/api/auth/login"
AUTH_USER_ENDPOINT = "/api/auth/user"
AUTH_LOGOUT_ENDPOINT = "/api/auth/logout"
AUTH_TOKEN_ENDPOINT = "/api/auth/token"

# Сообщения об ошибках
MSG_USER_ALREADY_EXISTS = "User already exists"
MSG_REQUIRED_FIELDS = "Email, password and name are required fields"
MSG_INCORRECT_CREDENTIALS = "email or password are incorrect"
MSG_UNAUTHORIZED = "You should be authorised"
MSG_INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
MSG_EMAIL_ALREADY_EXISTS = "User with such email already exists"

# Тестовые ингредиенты (валидные хеши из документации)
VALID_INGREDIENTS = [
    "6043b41abdacab0626a733c6",
    "609646e4dc916e00276b2870"
]

# Невалидный хеш для проверки ошибки 500
INVALID_INGREDIENT_HASH = "invalid_hash_123"