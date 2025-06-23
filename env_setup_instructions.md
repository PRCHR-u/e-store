# Настройка переменных окружения

## Обзор

Проект использует переменные окружения для безопасного хранения конфиденциальных данных и настройки различных параметров.

## Файлы

- `.env.example` - шаблон с примером переменных окружения
- `.env` - реальный файл с переменными (не отслеживается Git)
- `online_store/settings.py` - настроен для загрузки переменных из `.env`

## Установка

1. Скопируйте шаблон:
   ```bash
   cp .env.example .env
   ```

2. Отредактируйте файл `.env` с вашими настройками

## Переменные окружения

### Django Settings
- `SECRET_KEY` - секретный ключ Django (обязательно изменить в продакшене)
- `DEBUG` - режим отладки (True/False)
- `ALLOWED_HOSTS` - разрешенные хосты (через запятую)

### Database Settings (PostgreSQL)
- `DB_ENGINE` - движок базы данных
- `DB_NAME` - имя базы данных
- `DB_USER` - пользователь базы данных
- `DB_PASSWORD` - пароль базы данных
- `DB_HOST` - хост базы данных
- `DB_PORT` - порт базы данных

### Static and Media Files
- `STATIC_URL` - URL для статических файлов
- `MEDIA_URL` - URL для медиа файлов

### Security Settings
- `CSRF_TRUSTED_ORIGINS` - доверенные источники для CSRF

## Безопасность

⚠️ **ВАЖНО**: 
- Никогда не коммитьте файл `.env` в Git
- Файл `.env` уже добавлен в `.gitignore`
- В продакшене используйте сильный SECRET_KEY
- Храните пароли в безопасном месте

## Пример использования

```python
import os
from dotenv import load_dotenv

load_dotenv()

database_name = os.getenv('DB_NAME', 'default_db')
debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
```

## Генерация SECRET_KEY

Для генерации нового SECRET_KEY используйте:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Проверка настроек

После создания `.env` файла проверьте, что Django корректно загружает переменные:

```bash
python manage.py check
``` 