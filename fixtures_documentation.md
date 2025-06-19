# Документация по фикстурам

## Обзор

Созданы фикстуры для быстрого заполнения базы данных тестовыми данными для моделей `Category` и `Product`.

## Структура фикстур

### 📁 Папка: `catalog/fixtures/`

- `categories.json` - фикстура только для категорий (8 категорий)
- `products.json` - фикстура только для продуктов (18 продуктов)
- `initial_data.json` - общая фикстура с категориями и продуктами (5 категорий + 6 продуктов)

## Загрузка фикстур

### 1. Загрузка всех данных (рекомендуется)

```bash
python manage.py loaddata initial_data
```

### 2. Загрузка только категорий

```bash
python manage.py loaddata categories
```

### 3. Загрузка только продуктов

```bash
python manage.py loaddata products
```

### 4. Загрузка нескольких фикстур

```bash
python manage.py loaddata categories products
```

## Содержимое фикстур

### Категории (categories.json)

1. **Электроника** - Товары электронной техники и гаджеты
2. **Одежда** - Мужская и женская одежда, обувь, аксессуары
3. **Книги** - Художественная и техническая литература
4. **Спорт** - Спортивные товары, инвентарь и экипировка
5. **Дом и сад** - Товары для дома, сада и ремонта
6. **Красота и здоровье** - Косметика, парфюмерия, товары для здоровья
7. **Автотовары** - Автозапчасти, аксессуары и товары для автомобилей
8. **Игрушки и хобби** - Детские игрушки, настольные игры, товары для хобби

### Продукты (products.json)

#### Электроника:
- Смартфон iPhone 15 Pro (99,999.99 руб.)
- Ноутбук Dell XPS 13 (129,999.99 руб.)
- Беспроводные наушники Sony WH-1000XM5 (29,999.99 руб.)

#### Одежда:
- Футболка мужская хлопковая (1,999.99 руб.)
- Джинсы женские Levi's 501 (5,999.99 руб.)
- Кроссовки Nike Air Max (8,999.99 руб.)

#### Книги:
- Книга 'Война и мир' Л.Н. Толстой (899.99 руб.)
- Книга 'Мастер и Маргарита' М.А. Булгаков (799.99 руб.)

#### Спорт:
- Футбольный мяч Adidas Champions League (3,999.99 руб.)
- Велосипед горный Trek Marlin 7 (45,999.99 руб.)

#### Дом и сад:
- Горшок для цветов керамический (599.99 руб.)
- Набор инструментов Bosch (15,999.99 руб.)

#### Красота и здоровье:
- Крем для лица La Roche-Posay (1,299.99 руб.)
- Витамины Centrum (899.99 руб.)

#### Автотовары:
- Автомобильное масло Mobil 1 (2,499.99 руб.)
- Автомобильный коврик (799.99 руб.)

#### Игрушки и хобби:
- Настольная игра 'Монополия' (1,999.99 руб.)
- Конструктор LEGO Technic (5,999.99 руб.)

## Создание собственных фикстур

### Экспорт существующих данных

```bash
# Экспорт всех категорий
python manage.py dumpdata catalog.Category --indent=2 > my_categories.json

# Экспорт всех продуктов
python manage.py dumpdata catalog.Product --indent=2 > my_products.json

# Экспорт конкретной категории с её продуктами
python manage.py dumpdata catalog.Category catalog.Product --indent=2 > category_with_products.json
```

### Структура JSON фикстуры

```json
[
  {
    "model": "catalog.category",
    "pk": 1,
    "fields": {
      "name": "Название категории",
      "description": "Описание категории",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  },
  {
    "model": "catalog.product",
    "pk": 1,
    "fields": {
      "name": "Название продукта",
      "description": "Описание продукта",
      "image": "",
      "category": 1,
      "price": "999.99",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
]
```

## Очистка базы данных

### Удаление всех данных

```bash
python manage.py shell
```

```python
from catalog.models import Category, Product
Product.objects.all().delete()
Category.objects.all().delete()
```

### Сброс и загрузка фикстур

```bash
# Очистка и загрузка
python manage.py flush --noinput
python manage.py loaddata initial_data
```

## Использование в тестах

### Настройка тестов с фикстурами

```python
from django.test import TestCase

class CatalogTestCase(TestCase):
    fixtures = ['initial_data']
    
    def test_category_count(self):
        from catalog.models import Category
        self.assertEqual(Category.objects.count(), 5)
    
    def test_product_count(self):
        from catalog.models import Product
        self.assertEqual(Product.objects.count(), 6)
```

## Проверка загруженных данных

### Через Django shell

```bash
python manage.py shell
```

```python
from catalog.models import Category, Product

# Проверка количества
print(f"Категорий: {Category.objects.count()}")
print(f"Продуктов: {Product.objects.count()}")

# Просмотр категорий
for cat in Category.objects.all():
    print(f"{cat.id}: {cat.name}")

# Просмотр продуктов
for prod in Product.objects.all():
    print(f"{prod.id}: {prod.name} - {prod.price} руб.")
```

### Через админ-панель

1. Запустите сервер: `python manage.py runserver`
2. Откройте: `http://localhost:8000/admin/`
3. Войдите в админ-панель
4. Проверьте разделы "Категории" и "Товары"

## Примечания

- Фикстуры используют фиксированные даты создания (2024-01-01)
- Поля изображений оставлены пустыми
- Цены указаны в рублях с двумя знаками после запятой
- Связи между продуктами и категориями установлены корректно
- Все данные готовы для использования в разработке и тестировании 