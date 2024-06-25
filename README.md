# API для проекта YaMDb

### Описание

**YaMDb** - это каталог произведений искусства и отзывов к ним. Сами произведения в нём не хранятся, только их названия, характеристики, отзывы и оценки проставленные пользователями. Произведения разделены на категории (книги, фильмы, музыка...) и могут иметь жанры (сказка, рок, артхаус...).  
Любой человек может просматривать размещённую в сервисе информацию, а ставить произведениям оценки, писать отзывы и комментарии только аутентифицированные пользователи.  
Размещать и редактировать произведения и их характеристики могут только администраторы сервиса.  
Также, в сервисе предусмотрены модераторы, которые могут удалять и редактировать любые отзывы и комментарии.  
С помощью API можно управлять содержимым сервиса, просматривать информацию и создавать пользователей с любой ролью.
Для различных операций необходимо обладать подходящей ролью.

Все ресурсы API будут доступны по адресу http://127.0.0.1:8000/redoc/ после запуска проекта.

### Технологии:
requests==2.26.0
Django==3.2
djangorestframework==3.12.4
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
djangorestframework-simplejwt==4.7.2
django-filter==23.2

### Запуск проекта

- Клонировать репозиторий и перейти в него в командной строке:  
   `git clone git@github.com:Xenia387/api_yamdb.git`  
  `cd api_yamdb`

- Cоздать и активировать виртуальное окружение:  
   `python3 -m venv env source env/bin/activate`
  или
   `python -m venv env source venv/Scripts/activate`

- Установить зависимости из файла requirements.txt:  
   `python3 -m pip install --upgrade pip pip install -r requirements.txt`

- Выполнить миграции:  
   `python3 manage.py migrate`

- Запустить проект:  
   `python3 manage.py runserver`

### Начало работы с API:

- Запрос на получения кода подвтерждения для получения токена авторизации:

```
POST: http://127.0.0.1:8000/api/v1/auth/signup/
Body: {
    "username": "username",
    "email": "xxx@yyy.zz"
}
```

при успешном запросе, на указанный email придёт код подтверждения (_confirmation_code_).

- Для получения токена (_token_) необходимо передать полученный код подтверждения:

```
POST: http://127.0.0.1:8000/api/v1/auth/token/
Body: {
    "username": "username",
    "confirmation_code": "confirmation_code"
}
```

- Для аутентификации, в запросах следует использовать полученный токен:  
   в Headers указать следующее: `{"Authorization": "Bearer {token}"}`

* После аутентификации можно пользоваться [всеми ресурсами API](http://127.0.0.1:8000/redoc/), которые доступны для Вашей пользовательской роли. Без аутентификации доступен только просмотр основного контента.

Наполнение базы данных из csv-файлов с помощью management-команды можно выполнить:

python manage.py <название файла, в котором описана нужна команда>

Нужный файл можно найти в директории management/commands/

### Авторы:

Анисимова Ксения - https://github.com/Xenia387
email: anis.xenia@yandex.ru
telegram: @Ksenia_An_mova

Андреев Алексей - https://github.com/andreeval
Сергей Епифанов - https://github.com/segaru7
