Список доступных запросов к API:
    Теги:
        Список тегов GET: http://127.0.0.1:8000/api/tags/
        Получение тега GET: http://127.0.0.1:8000/api/tags/{id}/

    Ингридиенты:
        Список ингридиентов GET: http://127.0.0.1:8000/api/ingredients/
        Полуение ингридиента GET: http://127.0.0.1:8000/api/ingredients/{id}/


    Рецепты:
        Список рецептов:
        Создание рецепта POST: http://127.0.0.1:8000/api/recipes/
            {
                 "ingredients": [
                    {
                        "id": 1123,
                        "amount": 10
                    }
                ],
                "tags": [
                    1,
                    2
                ],
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                "name": "string",
                "text": "string",
                "cooking_time": 1
            }

        Получение рецепта:
        Обновление рецепта:
        Удаление рецепта:
        Получить короткую ссылку на рецепт:

    Пользователи:
        Список пользователей GET: http://127.0.0.1:8000/api/users/
        Регистрация пользователя POST: http://127.0.0.1:8000/api/users/
            {
                "email": "vpupkin@yandex.ru",
                "username": "vasya.pupkin",
                "first_name": "Вася",
                "last_name": "Иванов",
                "password": "Qwerty123"
            }
        Профиль пользователя GET: http://127.0.0.1:8000/api/users/{id}/
        Текущий пользователь GET: http://127.0.0.1:8000/api/users/me/
        Добавление аватара PUT: http://127.0.0.1:8000/api/users/me/avatar/
            {
                "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
            }
        Удаление аватара DEL: http://127.0.0.1:8000/api/users/me/avatar/
        Изменение пароля POST: http://127.0.0.1:8000/api/users/set_password/
            {
                "new_password": "string",
                "current_password": "string"
            }
        Получить токен авторизации POST: http://127.0.0.1:8000/api/auth/token/login/
            {
                "password": "string",
                "email": "string"
            }
        Удаление токена POST: http://127.0.0.1:8000/api/auth/token/logout/