#!/bin/bash

# Встановлюємо залежності
pip install -r requirements.txt

# Виконуємо міграції бази даних
python manage.py migrate

# Збираємо статичні файли
python manage.py collectstatic --noinput