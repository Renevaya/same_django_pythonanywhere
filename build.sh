#!/usr/bin/env bash
# Выходить при любой ошибке
set -o errexit

# Установка зависимостей
pip install -r requirements.txt

# Сборка статических файлов
python manage.py collectstatic --no-input

# Применение миграций базы данных к PostgreSQL на Render
python manage.py migrate

python manage.py createsuperuser --no-input || true

python -c "
import django
import os
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='ваш_логин').exists():
    User.objects.create_superuser('ваш_логин', 'ваш_email@example.com', 'ваш_пароль')
    print('суперпользователь создан')
else:
    print('суперпользователь уже существует')
"