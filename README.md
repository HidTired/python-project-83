### Hexlet tests and linter status:
[![Actions Status](https://github.com/HidTired/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/HidTired/python-project-83/actions)

# Анализатор веб-сайтов
# 📋 Подробная инструкция по установке и запуску
## Предварительные требования
Python 3.8+

PostgreSQL 16 (или новее)

pgAdmin 4 (для управления БД)

# 🔧Установка PostgreSQL (Windows)

## Скачайте установщик:

https://www.postgresql.org/download/windows/
↓ Windows x86-64 ↓ PostgreSQL 16 ↓ Download

## 🔧Настройка базы данных

Запустите pgAdmin 4 (из меню Пуск)

### Подключитесь к серверу:


Правый клик Servers → Register → Server

Name: localhost

Host: localhost

Username: postgres

Password: Введите ваш пароль и запомните его!

Save → Connect ✅

### Создайте БД page_analyzer:

Правый клик Databases → Create → Database

Database: page_analyzer → Save

### Создайте таблицы (Query Tool):

-- Удаляем старые (если есть)
```
DROP TABLE IF EXISTS url_checks;

DROP TABLE IF EXISTS urls;
```
CREATE TABLE urls (

    id SERIAL PRIMARY KEY,

    name VARCHAR UNIQUE NOT NULL,

    created_at DATE NOT NULL

);

CREATE TABLE url_checks (

    id SERIAL PRIMARY KEY,

    url_id INTEGER REFERENCES urls(id),

    status_code INTEGER,

    h1 TEXT,

    title TEXT,

    description TEXT,

    created_at DATE NOT NULL

);

### Проверяем
\dt

# Установка Python-зависимостей
## Клонируйте/распакуйте проект
cd python-project-83

## Установите зависимости
pip install -r requirements.txt

## Настройка .env
Скопируйте .env.example → .env

### Сгенерируйте SECRET_KEY:

python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(24))"
### Отредактируйте .env:

SECRET_KEY=ваш_сгенерированный_ключ_здесь
DATABASE_URL=postgresql://postgres:<ваш пароль>@localhost:5432/page_analyzer

# Запуск приложения

python page_analyzer/app.py

# Тестирование функционала
### Откройте: 
http://127.0.0.1:5000/


ВВедите URL 


Нажмите на URL ссылку


Нажмите на 'Запустить проверку'

## Очистка данных
В интерфейсе:

Главная → [🗑️ Очистить БД] → "База данных очищена!"
