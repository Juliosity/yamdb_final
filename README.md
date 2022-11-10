# yamdb_final

 ![yamdb workflow](https://github.com/Juliosity/yamdb_final/workflows/yamdb_workflow/badge.svg)

# Используемый стек
<p>
  <a 
  target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-_3.7-green.svg">
  </a>
  <a 
  target="_blank" href="https://www.djangoproject.com/download/" title="Django Framework"><img src="https://img.shields.io/badge/django-2.2-orange">
  </a>
  <a 
  target="_blank" href="https://www.django-rest-framework.org/" title="Django REST Framework"><img src="https://img.shields.io/badge/DRF-3.12-blue">
  </a>
  <a 
  target="_blank" href="https://django-filter.readthedocs.io/en/stable/" title="Django-filter"><img src="https://img.shields.io/badge/django--filter-21.1-brightgreen">
  </a>
  <a 
  target="_blank" href="https://django-rest-framework-simplejwt.readthedocs.io/en/latest/" title="JWT"><img src="https://img.shields.io/badge/DRF--SimpleJWT-5.0-red">
  </a>
</p>

# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

### Шаблон наполнения env-файла

```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=secretkey
```
### Запуск приложения в контейнерах

Запуск docker-compose:

```bash
docker-compose up -d
```
Выполнить миграции:

```bash
docker-compose exec web python manage.py migrate
```

Создать суперюзера:

```bash
docker-compose exec web python manage.py createsuperuser
```

Собрать статику:

```bash
docker-compose exec web python manage.py collectstatic --no-input
```

### Заполнение базы данными

```bash
docker-compose exec web python manage.py loaddata fixtures.json
```

### Сервер проекта
```bash
https://thejuliosity.gotdns.ch/admin
```

Команда разработки:
#### [Ярослав Филиппов](https://github.com/PhilYaren)
#### [Юлия Суркова](https://github.com/Juliosity)
