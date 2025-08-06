# Настройка Redis для Django проекта

## Статус подключения

✅ **Redis успешно подключен и работает!**

## Конфигурация

### 1. Установленные пакеты
- `django-redis==5.4.0` - интеграция Django с Redis
- `redis==5.0.1` - Python клиент для Redis

### 2. Настройки Django (`online_store/settings.py`)

```python
# Cache settings
CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'

if CACHE_ENABLED:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
```

### 3. Переменные окружения (`.env`)

```env
# Redis Settings
REDIS_URL=redis://127.0.0.1:6379/1
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_DB=1

# Cache Settings
CACHE_ENABLED=True
```

## Установка Redis на Windows

### Способ 1: Прямая установка
1. Скачайте Redis для Windows: https://github.com/microsoftarchive/redis/releases
2. Установите через MSI инсталлер
3. Redis будет доступен как служба Windows

### Способ 2: Запуск вручную
```powershell
# Скачать Redis
Invoke-WebRequest -Uri "https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.msi" -OutFile "Redis-x64-3.0.504.msi"

# Установить
Start-Process msiexec.exe -Wait -ArgumentList '/I Redis-x64-3.0.504.msi /quiet'

# Запустить Redis сервер
redis-server.exe
```

## Тестирование подключения

### 1. Проверка Redis CLI
```bash
redis-cli ping
# Должен вернуть: PONG
```

### 2. Тест через Python
```python
import redis
r = redis.Redis(host='127.0.0.1', port=6379, db=1)
print(r.ping())  # True
```

### 3. Тест через Django
```python
from django.core.cache import cache
cache.set('test_key', 'test_value', 60)
print(cache.get('test_key'))  # 'test_value'
```

### 4. Запуск тестового скрипта
```bash
python test_redis.py
```

## Использование кеширования в проекте

### Уровни кеширования

#### 1. 🏗️ Низкоуровневое кеширование (Model Managers)
- **Категории**: `Category.objects.get_cached_categories()`
- **Продукты**: `Product.objects.get_published_products()`
- **Продукты по категории**: `Product.objects.get_products_by_category(category_id)`
- **Отдельный продукт**: `Product.objects.get_product_by_id(product_id)`

#### 2. 🎯 Сервисное кеширование (Services)
- **Все продукты**: `get_all_products()`
- **Продукты по категории**: `get_products_by_category()`
- **Продукты по владельцу**: `get_products_by_owner()`
- **Продукты по диапазону цен**: `get_products_by_price_range()`
- **Категории с количеством продуктов**: `get_all_categories_with_products()`

#### 3. 🌐 Представления (Views)
- **Главная страница** (`/`) - кеширование списка продуктов
- **Детальная страница продукта** (`/product/<id>/`) - кеширование полного HTML-ответа
- **Страницы категорий** (`/category/<id>/`) - кеширование продуктов по категории
- **Страница категории** (`/category/<category_id>/`) - отдельное представление с пагинацией

#### 4. 📋 Контекстные процессоры
- **Список категорий** - кеширование в контекстном процессоре

#### 5. 🎨 Шаблоны и навигация
- **Базовый шаблон** (`base.html`) - включает меню с категориями
- **Меню навигации** (`menu.html`) - выпадающий список категорий
- **Шаблон категории** (`category_products.html`) - отображение продуктов с пагинацией
- **URL-маршруты** - `/category/<category_id>/` для страниц категорий

### 5. Кеширование в представлениях (`catalog/views.py`)

#### Кеширование главной страницы
```python
from django.core.cache import cache

class HomeView(ListView):
    def get_queryset(self):
        cache_key = "home_products_published"
        cached_products = cache.get(cache_key)
        if cached_products is not None:
            return cached_products
        
        products = Product.objects.filter(is_published=True)
        cache.set(cache_key, products, 600)  # 10 минут
        return products
```

#### Кеширование детальной страницы продукта
```python
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        # Кеширование на уровне представления
        cache_key = f"product_detail_{self.kwargs.get('pk')}"
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return cached_response
        
        response = super().get(request, *args, **kwargs)
        # Кешируем на 15 минут
        cache.set(cache_key, response, 60 * 15)
        return response
```

#### Кеширование страницы категории
```python
class CategoryProductsView(ListView):
    """Представление для отображения продуктов по категории"""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id=category_id, only_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        from .models import Category
        context['category'] = get_object_or_404(Category, id=category_id)
        # Используем кешированные категории из контекстного процессора
        context['categories'] = get_all_categories_with_products()
        return context
```

### 6. Шаблоны и навигация

#### Базовый шаблон (`catalog/templates/catalog/base.html`)
```html
<!doctype html>
<html lang="ru">
<head>
    <title>{% block title %}Online Store{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <header class="bg-primary text-white py-3 mb-4">
        <div class="container">
            <h1>Online Store</h1>
        </div>
    </header>

    {% include 'catalog/menu.html' %}

    <main class="container mb-5">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

#### Меню навигации (`catalog/templates/catalog/menu.html`)
```html
<nav class="navbar navbar-expand-lg navbar-light bg-light mb-4">
  <div class="container">
    <a class="navbar-brand" href="/">Главная</a>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown">
            Категории
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            {% for category in categories %}
            <li>
              <a class="dropdown-item d-flex justify-content-between align-items-center" 
                 href="{% url 'category_products' category_id=category.id %}">
                {{ category.name }}
                <span class="badge bg-primary rounded-pill">{{ category.products_count }}</span>
              </a>
            </li>
            {% endfor %}
          </ul>
        </li>
      </ul>
    </div>
  </div>
</nav>
```

#### Шаблон категории (`catalog/templates/catalog/category_products.html`)
```html
{% extends 'catalog/base.html' %}

{% block title %}{{ category.name }} - Online Store{% endblock %}

{% block content %}
<div class="row">
    <!-- Боковая панель с категориями -->
    <div class="col-md-3">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Категории</h5>
            </div>
            <div class="card-body">
                <div class="list-group list-group-flush">
                    {% for cat in categories %}
                    <a href="{% url 'category_products' category_id=cat.id %}" 
                       class="list-group-item list-group-item-action {% if cat.id == category.id %}active{% endif %}">
                        {{ cat.name }}
                        <span class="badge bg-primary rounded-pill">{{ cat.products_count }}</span>
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>

    <!-- Основной контент -->
    <div class="col-md-9">
        <h2>{{ category.name }}</h2>
        
        {% if products %}
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            {% for product in products %}
            <div class="col">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">{{ product.name }}</h5>
                        <p class="card-text">{{ product.description|truncatewords:20 }}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="h5 text-primary mb-0">{{ product.price }} ₽</span>
                            <a href="{% url 'product_detail' pk=product.pk %}" class="btn btn-outline-primary btn-sm">
                                Подробнее
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- Пагинация -->
        {% if is_paginated %}
        <nav aria-label="Навигация по страницам" class="mt-4">
            <ul class="pagination justify-content-center">
                {% if page_obj.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Предыдущая</a>
                </li>
                {% endif %}

                <li class="page-item active">
                    <span class="page-link">
                        Страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}
                    </span>
                </li>

                {% if page_obj.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ page_obj.next_page_number }}">Следующая</a>
                </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}

        {% else %}
        <div class="text-center py-5">
            <h4 class="text-muted">В данной категории пока нет товаров</h4>
            <a href="{% url 'home' %}" class="btn btn-primary">Вернуться на главную</a>
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

### 2. Низкоуровневое кеширование в моделях (`catalog/models.py`)

#### CategoryManager
```python
class CategoryManager(models.Manager):
    def get_cached_categories(self):
        """Получает все категории с кешированием"""
        cache_key = "all_categories"
        cached_categories = cache.get(cache_key)
        if cached_categories is not None:
            return cached_categories
        
        categories = self.all().order_by('name')
        cache.set(cache_key, categories, 1800)  # 30 минут
        return categories
    
    def get_categories_with_products_count(self, only_published=True):
        """Получает категории с количеством продуктов"""
        cache_key = f"categories_with_count_{'published' if only_published else 'all'}"
        cached_categories = cache.get(cache_key)
        if cached_categories is not None:
            return cached_categories
        
        from django.db.models import Count
        categories = self.annotate(
            products_count=Count('products', filter=models.Q(products__is_published=True) if only_published else None)
        ).filter(products_count__gt=0).order_by('name')
        
        cache.set(cache_key, categories, 900)  # 15 минут
        return categories
```

#### ProductManager
```python
class ProductManager(models.Manager):
    def get_published_products(self):
        """Получает опубликованные продукты с кешированием"""
        cache_key = "published_products"
        cached_products = cache.get(cache_key)
        if cached_products is not None:
            return cached_products
        
        products = self.filter(is_published=True).select_related('category', 'owner').order_by('-created_at')
        cache.set(cache_key, products, 600)  # 10 минут
        return products
    
    def get_products_by_category(self, category_id, only_published=True):
        """Получает продукты по категории с кешированием"""
        cache_key = f"products_by_category_{category_id}_{'published' if only_published else 'all'}"
        cached_products = cache.get(cache_key)
        if cached_products is not None:
            return cached_products
        
        products = self.filter(category_id=category_id)
        if only_published:
            products = products.filter(is_published=True)
        
        products = products.select_related('category', 'owner').order_by('-created_at')
        cache.set(cache_key, products, 600)  # 10 минут
        return products
```

### 3. Кеширование в сервисах (`catalog/services.py`)

#### Основные сервисные функции
```python
def get_all_products(only_published=True):
    """Получение всех продуктов"""
    if only_published:
        return Product.objects.get_published_products()
    else:
        return Product.objects.select_related('category', 'owner').order_by('-created_at')

def get_products_by_category(category_id=None, category_slug=None, only_published=True):
    """Получение продуктов по категории"""
    if category_id:
        return Product.objects.get_products_by_category(category_id, only_published)
    # ... остальная логика

def get_products_by_owner(owner_id, only_published=True):
    """Получение продуктов по владельцу"""
    cache_key = f"products_by_owner_{owner_id}_{'published' if only_published else 'all'}"
    cached_products = cache.get(cache_key)
    if cached_products is not None:
        return cached_products
    
    products = Product.objects.filter(owner_id=owner_id)
    if only_published:
        products = products.filter(is_published=True)
    
    products = products.select_related('category', 'owner').order_by('-created_at')
    cache.set(cache_key, products, 600)  # 10 минут
    return products

def get_products_by_price_range(min_price=None, max_price=None, only_published=True):
    """Получение продуктов по диапазону цен"""
    cache_key = f"products_by_price_{min_price}_{max_price}_{'published' if only_published else 'all'}"
    cached_products = cache.get(cache_key)
    if cached_products is not None:
        return cached_products
    
    products = Product.objects.all()
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)
    
    if only_published:
        products = products.filter(is_published=True)
    
    products = products.select_related('category', 'owner').order_by('-created_at')
    cache.set(cache_key, products, 600)  # 10 минут
    return products

def get_all_categories_with_products(only_published=True):
    """Получение категорий с количеством продуктов"""
    return Category.objects.get_categories_with_products_count(only_published)
```

### 4. Инвалидация кеша

```python
def invalidate_products_cache(category_id=None, product_id=None):
    cache_keys = []
    
    if product_id:
        # Инвалидируем кеш детальной страницы продукта
        cache_keys.append(f"product_detail_{product_id}")
    
    if category_id:
        # Инвалидируем кеш конкретной категории
        cache_keys.extend([
            f"products_category_{category_id}_published",
            f"products_category_{category_id}_all"
        ])
    else:
        # Инвалидируем все кеши продуктов и категорий
        cache_keys.extend([
            "home_products_published",
            "categories_with_products_published",
            "categories_with_products_all"
        ])
    
    for key in cache_keys:
        cache.delete(key)
```

## Команды управления кешем

### Очистка всего кеша продуктов
```bash
python manage.py clear_products_cache
```

### Очистка кеша конкретной категории
```bash
python manage.py clear_products_cache --category-id 1
```

## Мониторинг Redis

### 1. Подключение к Redis CLI
```bash
redis-cli
```

### 2. Основные команды
```bash
# Информация о сервере
INFO

# Список всех ключей
KEYS *

# Информация о памяти
INFO memory

# Мониторинг команд в реальном времени
MONITOR
```

### 3. Очистка базы данных
```bash
# Очистить текущую базу
FLUSHDB

# Очистить все базы
FLUSHALL
```

## Производительность

### Результаты тестирования низкоуровневого кеширования:

#### Категории
- ⏱️ Первый запрос (без кеша): 0.1869 сек
- ⏱️ Второй запрос (с кеша): 0.0004 сек
- 🚀 Ускорение: 495x

#### Продукты
- ⏱️ Первый запрос (без кеша): 0.2011 сек
- ⏱️ Второй запрос (с кеша): 0.0003 сек
- 🚀 Ускорение: 760x

#### Сервисное кеширование
- ⏱️ Первый запрос (без кеша): 0.1810 сек
- ⏱️ Второй запрос (с кеша): 0.0004 сек
- 🚀 Ускорение: 444x

## Управление кешированием

### Включение/отключение кеширования

Кеширование можно включать и отключать через переменную окружения `CACHE_ENABLED`:

```env
# Включить кеширование (по умолчанию)
CACHE_ENABLED=True

# Отключить кеширование
CACHE_ENABLED=False
```

### Проверка статуса кеширования

```python
from django.conf import settings

# Проверить, включено ли кеширование
print(settings.CACHE_ENABLED)  # True/False

# Проверить тип кеша
print(settings.CACHES['default']['BACKEND'])
# При включенном кеше: django_redis.cache.RedisCache
# При отключенном кеше: django.core.cache.backends.dummy.DummyCache
```

### Временное отключение кеширования

```bash
# В PowerShell
$env:CACHE_ENABLED="False"; python manage.py runserver

# В командной строке
set CACHE_ENABLED=False && python manage.py runserver
```

## Troubleshooting

### Проблема: Redis не запускается
**Решение:**
1. Проверьте, что Redis установлен
2. Запустите вручную: `redis-server.exe`
3. Проверьте порт 6379 на занятость

### Проблема: Django не подключается к Redis
**Решение:**
1. Проверьте настройки в `settings.py`
2. Убедитесь, что Redis запущен
3. Проверьте переменные окружения

### Проблема: Кеш не работает
**Решение:**
1. Проверьте подключение: `python -c "import redis; r = redis.Redis(); print(r.ping())"`
2. Проверьте настройки Django
3. Очистите кеш: `python manage.py clear_products_cache`

## Дополнительные возможности

### 1. Сессии в Redis
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### 2. Кеширование шаблонов
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]
```

### 3. Кеширование запросов к БД
```python
from django.core.cache import cache

def get_expensive_data():
    cache_key = 'expensive_data'
    data = cache.get(cache_key)
    if data is None:
        data = perform_expensive_operation()
        cache.set(cache_key, data, 3600)  # 1 час
    return data
``` 