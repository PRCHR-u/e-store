# Настройка PostgreSQL для Django проекта

## После установки PostgreSQL

1. **Подключитесь к PostgreSQL**:
   ```bash
   psql -U postgres -h localhost
   ```

2. **Создайте базу данных**:
   ```sql
   CREATE DATABASE online_store_db;
   ```

3. **Проверьте создание базы данных**:
   ```sql
   \l
   ```

4. **Выйдите из psql**:
   ```sql
   \q
   ```

## Настройки в Django

Файл `settings.py` уже настроен для подключения к PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'online_store_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Применение миграций

После создания базы данных выполните:

```bash
python manage.py migrate
```

## Проверка подключения

Для проверки подключения выполните:

```bash
python manage.py dbshell
``` 