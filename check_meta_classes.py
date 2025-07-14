#!/usr/bin/env python
"""
Скрипт для проверки Meta классов в моделях Django
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from catalog.models import Category, Product

def check_meta_classes():
    """Проверка Meta классов в моделях"""
    print("=" * 50)
    print("ПРОВЕРКА META КЛАССОВ В МОДЕЛЯХ")
    print("=" * 50)
    
    # Проверка модели Category
    print("\n📁 МОДЕЛЬ Category:")
    print(f"  verbose_name: '{Category._meta.verbose_name}'")
    print(f"  verbose_name_plural: '{Category._meta.verbose_name_plural}'")
    print(f"  ordering: {Category._meta.ordering}")
    print(f"  Поля: {[field.name for field in Category._meta.fields]}")
    
    # Проверка модели Product
    print("\n📦 МОДЕЛЬ Product:")
    print(f"  verbose_name: '{Product._meta.verbose_name}'")
    print(f"  verbose_name_plural: '{Product._meta.verbose_name_plural}'")
    print(f"  ordering: {Product._meta.ordering}")
    print(f"  Поля: {[field.name for field in Product._meta.fields]}")
    
    # Проверка связей
    print("\n🔗 СВЯЗИ МЕЖДУ МОДЕЛЯМИ:")
    category_field = Product._meta.get_field('category')
    print(f"  Product.category -> {category_field.related_model.__name__}")
    print(f"  related_name: '{category_field.related_name}'")
    
    print("\n✅ ПРОВЕРКА ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 50)

def test_ordering():
    """Тестирование сортировки"""
    print("\n🔄 ТЕСТИРОВАНИЕ СОРТИРОВКИ:")
    
    # Тест сортировки категорий
    categories = Category.objects.all()
    print(f"  Категории (сортировка по name): {list(categories.values_list('name', flat=True))}")
    
    # Тест сортировки товаров
    products = Product.objects.all()
    print(f"  Товары (сортировка по -created_at): {list(products.values_list('name', 'created_at', flat=True))}")

if __name__ == "__main__":
    try:
        check_meta_classes()
        test_ordering()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Убедитесь, что база данных настроена и миграции применены") 