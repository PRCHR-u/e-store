import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from catalog.models import Category, Product

print("=== Django Shell Operations ===")

# 1. Создание категорий
print("\n1. Создание категорий:")
categories = [
    Category.objects.get_or_create(name='Электроника', defaults={'description': 'Товары электронной техники'})[0],
    Category.objects.get_or_create(name='Одежда', defaults={'description': 'Мужская и женская одежда'})[0],
    Category.objects.get_or_create(name='Книги', defaults={'description': 'Художественная литература'})[0],
]
for cat in categories:
    print(f"   - {cat.name}")

# 2. Создание продуктов
print("\n2. Создание продуктов:")
products = [
    Product.objects.get_or_create(
        name='Смартфон iPhone 15',
        defaults={'description': 'Новейший смартфон', 'category': categories[0], 'price': 89999.99}
    )[0],
    Product.objects.get_or_create(
        name='Футболка мужская',
        defaults={'description': 'Хлопковая футболка', 'category': categories[1], 'price': 1999.99}
    )[0],
    Product.objects.get_or_create(
        name='Книга "Война и мир"',
        defaults={'description': 'Классика', 'category': categories[2], 'price': 899.99}
    )[0],
]
for prod in products:
    print(f"   - {prod.name} ({prod.category.name}) - {prod.price} руб.")

# 3. Получение всех категорий
print("\n3. Все категории:")
for cat in Category.objects.all():
    print(f"   - {cat.id}: {cat.name}")

# 4. Получение всех продуктов
print("\n4. Все продукты:")
for prod in Product.objects.all():
    print(f"   - {prod.id}: {prod.name} - {prod.price} руб.")

# 5. Продукты в категории 'Электроника'
print("\n5. Продукты в категории 'Электроника':")
electronics = Category.objects.get(name='Электроника')
for prod in electronics.products.all():
    print(f"   - {prod.name}")

# 6. Обновление цены
print("\n6. Обновление цены:")
if products:
    old_price = products[0].price
    products[0].price = old_price * 1.1
    products[0].save()
    print(f"   Цена обновлена: {old_price} → {products[0].price} руб.")

# 7. Удаление продукта
print("\n7. Удаление продукта:")
if products:
    product_name = products[-1].name
    products[-1].delete()
    print(f"   Удален: {product_name}")

# 8. Статистика
print("\n8. Статистика:")
print(f"   Категорий: {Category.objects.count()}")
print(f"   Продуктов: {Product.objects.count()}")

print("\n=== Завершено ===")