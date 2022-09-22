[![CI](https://github.com/InsomniaTSO/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/InsomniaTSO/yamdb_final/actions/workflows/yamdb_workflow.yml)

# __Проект «API для Yamdb»__

## __Описание__:

API для оценки произведений (фильмов, книг, игр и т.п.).

## __Авторы__:

Матвей Бондаренко,
Назар Качура,
Татьяна Манакова.

## __Технологии__:

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [PostgreSQL](https://www.postgresql.org/)
* [Docker](https://www.docker.com/)
* [Gunicorn](https://gunicorn.org/)
* [Nginx](https://nginx.org/)

### __Шаблон наполнения env-файла__:

```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=xxxxxx # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxx # секретный ключ из settings.py 
```

## __Примеры запросов__:

Регистрация пользователя:

```
POST http://insomniatso.sytes.net/api/v1/auth/signup/
{
"email": "string",
"username": "string"
}
```
На указанную почту придет код подтверждения.

Получение токена:

```
POST http://insomniatso.sytes.net/api/v1/auth/token/
{
"confirmation_code": "string",
"username": "string"
}
```

Дополнение или изменение данных пользователя:

```
PATCH http://insomniatso.sytes.net/api/v1/users/me/
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string"
}
```

Оставить отзыв с оценкой:

```
POST http://insomniatso.sytes.net/api/v1/titles/{title_id}/reviews/
{
"text": "string",
"score": 1
}
```

## Ссылки

Проект доступен по ссылке <http://insomniatso.sytes.net/>
