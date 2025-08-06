# Документация по классам Meta в моделях

## Обзор

В моделях `Category` и `Product` настроены классы Meta с параметрами для корректного отображения в админ-панели Django.

## Модель Category

### Класс Meta
```python
class Meta:
    verbose_name = 'Категория'
    verbose_name_plural = 'Категории'
    ordering = ['name']
```

### Параметры:
- **verbose_name** = 'Категория' - единственное число для отображения в админ-панели
- **verbose_name_plural** = 'Категории' - множественное число для отображения в админ-панели
- **ordering** = ['name'] - сортировка по умолчанию по полю name

### Поля модели:
- `name` - CharField, максимальная длина 100 символов
- `description` - TextField, необязательное поле
- `created_at` - DateTimeField, автоматически заполняется при создании
- `updated_at` - DateTimeField, автоматически обновляется при изменении

## Модель Product

### Класс Meta
```python
class Meta:
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'
    ordering = ['-created_at']
```

### Параметры:
- **verbose_name** = 'Товар' - единственное число для отображения в админ-панели
- **verbose_name_plural** = 'Товары' - множественное число для отображения в админ-панели
- **ordering** = ['-created_at'] - сортировка по умолчанию по дате создания (новые сначала)

### Поля модели:
- `name` - CharField, максимальная длина 200 символов
- `description` - TextField, необязательное поле
- `image` - ImageField, необязательное поле для изображения
- `category` - ForeignKey к модели Category
- `price` - DecimalField, цена с двумя знаками после запятой
- `created_at` - DateTimeField, автоматически заполняется при создании
- `updated_at` - DateTimeField, автоматически обновляется при изменении

## Отображение в админ-панели

### CategoryAdmin
- **list_display**: ['id', 'name'] - отображаемые поля в списке
- **search_fields**: ['name', 'description'] - поля для поиска

### ProductAdmin
- **list_display**: ['id', 'name', 'price', 'category'] - отображаемые поля в списке
- **list_filter**: ['category'] - фильтр по категории
- **search_fields**: ['name', 'description'] - поля для поиска
- **list_select_related**: ['category'] - оптимизация запросов

## Преимущества использования Meta классов

1. **Локализация**: Русские названия в админ-панели
2. **Сортировка**: Автоматическая сортировка по умолчанию
3. **Читаемость**: Понятные названия для пользователей
4. **Консистентность**: Единообразное отображение во всем приложении

## Проверка настроек

Для проверки корректности настроек выполните:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

## Доступ к админ-панели

1. Создайте суперпользователя:
   ```bash
   python manage.py createsuperuser
   ```

2. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

3. Откройте админ-панель: http://127.0.0.1:8000/admin/

## Примеры использования

### Получение verbose_name
```python
from catalog.models import Category, Product

# Получить verbose_name модели
print(Category._meta.verbose_name)  # 'Категория'
print(Product._meta.verbose_name)   # 'Товар'

# Получить verbose_name_plural
print(Category._meta.verbose_name_plural)  # 'Категории'
print(Product._meta.verbose_name_plural)   # 'Товары'
```

### Использование ordering
```python
# Получить категории, отсортированные по имени
categories = Category.objects.all()  # автоматически сортируется по name

# Получить товары, отсортированные по дате создания (новые сначала)
products = Product.objects.all()  # автоматически сортируется по -created_at
``` 