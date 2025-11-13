# Настройка PostgreSQL для Django проекта - ЗАВЕРШЕНО ✅

## Статус: PostgreSQL успешно подключен!

PostgreSQL установлен и настроен для работы с Django проектом.

## Настройки подключения

Файл `settings.py` настроен для подключения к PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'online_store_db',
        'USER': 'postgres',
        'PASSWORD': '4aQ7u27Qb64RTVP',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Выполненные действия

1. ✅ **Установлен PostgreSQL 17**
2. ✅ **Создана база данных** `online_store_db`
3. ✅ **Установлен драйвер** `psycopg2-binary==2.9.9`
4. ✅ **Настроено подключение** в Django
5. ✅ **Применены миграции** к PostgreSQL
6. ✅ **Проверено подключение** Django к базе данных

## Команды для работы с базой данных

### Подключение к PostgreSQL через psql:
```powershell
$env:PGPASSWORD="4aQ7u27Qb64RTVP"; & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -h localhost
```

### Применение миграций Django:
```bash
python manage.py migrate
```

### Проверка подключения:
```bash
python manage.py check --database default
```

### Запуск сервера разработки:
```bash
python manage.py runserver
```

## Управление базой данных

Для графического управления базой данных используйте pgAdmin 4:
```powershell
& "C:\Program Files\PostgreSQL\17\pgAdmin 4\runtime\pgAdmin4.exe"
```

## Пароль для подключения

- **Пользователь:** `postgres`
- **Пароль:** `4aQ7u27Qb64RTVP`
- **База данных:** `online_store_db`
- **Хост:** `localhost`
- **Порт:** `5432` 