# FOODGRAM

# Описание проекта
Foodgram - это сайт с возможностью добавлять рецепты собственных блюд, просматривать рецепты других авторов. Так же имеется возможность подписаться на автора другого рецепта. Можно добавить любимые рецепты в категорию "избранное".

# Стек
* Python 3.9
* Django 3.2.3
* Djangorestframework 3.12.4
* Nginx
* Docker
* JWT
* Gunicorn

# Как развернуть проект на сервере
Как развернуть проект с помощью Docker.
1. Создать директории: ```mkdir foodgram``` и ```infra```
2. Перейти в них: ```cd foodgram```, далее ```cd infra```
3. Поместить в директорию файл: **docker-compose.production.yml**
4. Выполнить команду: ```docker compose -f docker-compose.production.yml up```
5. Собрать статику: ```docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic```
6. Копировать статику: ```docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/``` 
7. Выполнить миграции: ```docker compose -f docker-compose.production.yml exec backend python manage.py migrate```
8. Загрузить фикстуры с ингредиентами:  ```docker container exet -it foodgram-backend python manage.py load_fixture```

# Как развернуть проект локально
1. Копировать репозиторий
2. Создать файл .env и заполнить его приведенными ниже данными
3. Запустить докер контенеры, испоьзуя ```docker-compose -f docker-compose-local.yml up -d```
4. Выполнить команды по сборке статики, ее копированию. Выполнить миграции и запонить базу тестовыми данными. Аналогичные команды указаны выше.
5. Документация доступных эндпоинтов будет доступна по адресу  [http://localhost/api/docs/](http://localhost/api/docs/)

# Как заполнить env файл
Пример заполнения:
* POSTGRES_USER= Пользователь БД.
* POSTGRES_PASSWORD= Пароль от БД.
* POSTGRES_DB= Имя контейнера с БД.
* DB_HOST= Имя БД.
* DB_PORT= Порт для БД.
* SECRET_KEY= Ключ для настроек в джанго проекте.
* ALLOWED_HOSTS= Список доступных хостов. Пример: '127.0.0.1, ' 
* DEBUG = 'False/True' Режим отладки.

# Список доступных эндпоинтов
/api/users/
/api/users/{id}/
/api/users/me/
/api/users/set_password/
/api/auth/token/login/
/api/auth/token/logout/
/api/tags/
/api/tags/{id}/
/api/recipes/
/api/recipes/{id}/
/api/recipes/download_shopping_cart/
/api/recipes/{id}/shopping_cart/
/api/recipes/{id}/favorite/
/api/users/subscriptions/
/api/users/{id}/subscribe/
/api/ingredients/
/api/ingredients/{id}

# Примеры запросов 
POST /api/users/ - запрос на регистрацию нового пользователя.
```
{
"email": "vpupkin@yandex.ru",
"username": "vasya.pupkin",
"first_name": "Вася",
"last_name": "Пупкин",
"password": "Qwerty123"
}
```

POST /api/auth/token/login/ - запрос на получение токена.
```
{
"password": "Qwerty123",
"email": "vpupkin@yandex.ru"
}
```

POST /api/recipes/ - создание нового рецепта.
```
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
  "image": "binary",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```


# Автор
Автор проекта - Тихомиров Никита - https://github.com/NikTihomirovv
