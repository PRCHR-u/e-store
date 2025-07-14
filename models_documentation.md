# Документация моделей приложения Catalog

## Обзор

В приложении `catalog` созданы две основные модели для управления товарами и категориями:

## Модель Category (Категория)

### Поля:
- **name** (CharField, max_length=100) - Наименование категории
- **description** (TextField, blank=True) - Описание категории
- **created_at** (DateTimeField, auto_now_add=True) - Дата создания
- **updated_at** (DateTimeField, auto_now=True) - Дата последнего изменения

### Настройки:
- **verbose_name**: 'Категория'
- **verbose_name_plural**: 'Категории'
- **ordering**: ['name'] - сортировка по наименованию

### Связи:
- Имеет обратную связь `products` с моделью Product

## Модель Product (Товар)

### Поля:
- **name** (CharField, max_length=200) - Наименование товара
- **description** (TextField, blank=True) - Описание товара
- **image** (ImageField, upload_to='products/', blank=True, null=True) - Изображение товара
- **category** (ForeignKey to Category) - Категория товара
- **price** (DecimalField, max_digits=10, decimal_places=2) - Цена за покупку
- **created_at** (DateTimeField, auto_now_add=True) - Дата создания
- **updated_at** (DateTimeField, auto_now=True) - Дата последнего изменения

### Настройки:
- **verbose_name**: 'Товар'
- **verbose_name_plural**: 'Товары'
- **ordering**: ['-created_at'] - сортировка по дате создания (новые сначала)

### Связи:
- **category** - внешний ключ к модели Category с каскадным удалением
- **related_name**: 'products' - обратная связь для получения товаров категории

## Админ-панель

### CategoryAdmin:
- **list_display**: ['name', 'created_at', 'updated_at']
- **list_filter**: ['created_at', 'updated_at']
- **search_fields**: ['name', 'description']
- **readonly_fields**: ['created_at', 'updated_at']

### ProductAdmin:
- **list_display**: ['name', 'category', 'price', 'created_at', 'updated_at']
- **list_filter**: ['category', 'created_at', 'updated_at']
- **search_fields**: ['name', 'description']
- **readonly_fields**: ['created_at', 'updated_at']
- **list_select_related**: ['category'] - оптимизация запросов

## Настройки файлов

### Медиа-файлы:
- **MEDIA_URL**: '/media/'
- **MEDIA_ROOT**: BASE_DIR / 'media'
- **upload_to**: 'products/' - изображения сохраняются в папку media/products/

### URL-маршруты:
- Настроены маршруты для медиа-файлов в режиме разработки
- Добавлены в `online_store/urls.py`

## Использование

### Создание категории:
```python
category = Category.objects.create(
    name='Электроника',
    description='Товары электронной техники'
)
```

### Создание товара:
```python
product = Product.objects.create(
    name='Смартфон',
    description='Современный смартфон',
    category=category,
    price=29999.99
)
```

### Получение товаров категории:
```python
category.products.all()  # все товары категории
```

### Фильтрация товаров:
```python
Product.objects.filter(category__name='Электроника')
Product.objects.filter(price__gte=1000)
```

## Миграции

Создана и применена миграция `0001_initial.py` с таблицами:
- `catalog_category`
- `catalog_product`

База данных PostgreSQL готова к использованию. 