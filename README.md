
# BarterSystem

Платформа для обмена товарами между пользователями.  
Реализовано с использованием Django и PostgreSQL.

---

## Функциональность

- Регистрация и вход пользователей
- Создание, редактирование и удаление объявлений
- Просмотр всех объявлений (кроме своих)
- Отправка предложений обмена
- Отображение входящих и исходящих предложений
- Фильтрация объявлений и обменов по параметрам
- Пагинация
- Юнит-тесты

---

## Установка и запуск

### 1. Клонировать проект

```bash
git clone https://github.com/your_username/bartersystem.git
cd bartersystem
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить файл `.env`

Создайте файл `.env` в корне проекта и добавьте переменные:

```env
SECRET_KEY=ваш_секретный_ключ
DEBUG=True
```

## Настройка базы данных

По умолчанию используется PostgreSQL. Настройки находятся в `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bartersystem',
        'USER': 'postgres',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Запуск проекта

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

После запуска открой в браузере:  
http://127.0.0.1:8000

---

## Тестирование

Для запуска тестов моделей:

```bash
python manage.py test ads
```

Тестируются:

- Создание, редактирование, удаление объявлений
- Создание и фильтрация предложений обмена

---

