# Примеры использования Django shell для работы с моделями

## Подготовка
Сначала запустите Django shell:
```bash
python manage.py shell
```

## Импорт моделей
```python
from catalog.models import Category, Product
```

## 1. Получение всех категорий
```python
# Импортируем функцию
from django_shell_queries import get_all_categories

# Получаем все категории
categories = get_all_categories()

# Альтернативный способ (без форматированного вывода)
categories = Category.objects.all()
for category in categories:
    print(category.name)
```

## 2. Получение всех продуктов
```python
# Импортируем функцию
from django_shell_queries import get_all_products

# Получаем все продукты
products = get_all_products()

# Альтернативный способ (без форматированного вывода)
products = Product.objects.all()
for product in products:
    print(f"{product.name} - {product.price}")
```

## 3. Поиск продуктов в категории
```python
# Импортируем функцию
from django_shell_queries import get_products_by_category

# Получаем продукты в категории
category_products = get_products_by_category("Электроника")

# Альтернативный способ (без форматированного вывода)
try:
    category = Category.objects.get(name="Электроника")
    products = Product.objects.filter(category=category)
    for product in products:
        print(f"{product.name} - {product.price}")
except Category.DoesNotExist:
    print("Категория не найдена")
```

## 4. Обновление цены продукта
```python
# Импортируем функцию
from django_shell_queries import update_product_price

# Обновляем цену продукта
updated_product = update_product_price("Смартфон", 999.99)

# Альтернативный способ (без форматированного вывода)
try:
    product = Product.objects.get(name="Смартфон")
    old_price = product.price
    product.price = 999.99
    product.save()
    print(f"Цена обновлена: {old_price} -> {product.price}")
except Product.DoesNotExist:
    print("Продукт не найден")
```

## 5. Удаление продукта
```python
# Импортируем функцию
from django_shell_queries import delete_product

# Удаляем продукт
success = delete_product("Старый продукт")

# Альтернативный способ (без форматированного вывода)
try:
    product = Product.objects.get(name="Старый продукт")
    product.delete()
    print("Продукт удален")
except Product.DoesNotExist:
    print("Продукт не найден")
```

## Дополнительные примеры

### Создание новой категории
```python
new_category = Category.objects.create(
    name="Новая категория",
    description="Описание новой категории"
)
```

### Создание нового продукта
```python
category = Category.objects.get(name="Электроника")
new_product = Product.objects.create(
    name="Новый продукт",
    description="Описание нового продукта",
    price=499.99,
    category=category
)
```

### Фильтрация продуктов по цене
```python
# Продукты дороже 1000
expensive_products = Product.objects.filter(price__gt=1000)

# Продукты дешевле 500
cheap_products = Product.objects.filter(price__lt=500)

# Продукты в ценовом диапазоне
mid_range_products = Product.objects.filter(price__range=(500, 1000))
```

### Поиск по имени (частичное совпадение)
```python
# Продукты, содержащие "телефон" в названии
phones = Product.objects.filter(name__icontains="телефон")
```

### Сортировка
```python
# По возрастанию цены
sorted_by_price_asc = Product.objects.all().order_by('price')

# По убыванию цены
sorted_by_price_desc = Product.objects.all().order_by('-price')

# По имени и цене
sorted_by_name_and_price = Product.objects.all().order_by('name', 'price')
``` 