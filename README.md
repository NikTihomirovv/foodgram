# FOODGRAM

# Описание проекта
Foodgram - это сайт с возможностью добавлять рецепты собственных блюд, просматривать рецепты других авторов. Так же имеется возможность подписаться на автора другого рецепта. Можно добавить любимые рецепты в категорию "избранное".

# Стек
* Python 3.9
* Django 3.2.3
* djangorestframework 3.12.4
* Nginx
* Docker

# Как развернуть проект
Как развернуть проект с помощью Docker.
1. Создать директории: ```mkdir foodgram``` и ```infra```
2. Перейти в них: ```cd foodgram```, далее ```cd infra```
3. Поместить в директорию файл: **docker-compose.production.yml**
4. Выполнить команду: ```docker compose -f docker-compose.production.yml up```
5. Собрать статику: ```docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic```
6. Копировать статику: ```docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/``` 
7. Выполнить миграции: ```docker compose -f docker-compose.production.yml exec backend python manage.py migrate```
8. Загрузить фикстуры с ингредиентами:  ```docker container exet -it foodgram-backend python manage.py load_fixture```

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

# Автор
Автор проекта - Тихомиров Никита - https://github.com/NikTihomirovv
