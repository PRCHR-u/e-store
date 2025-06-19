#!/usr/bin/env python
"""
Скрипт для проверки настроек медиа файлов в Django
"""

import os
import django
from pathlib import Path

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from django.conf import settings
from catalog.models import Product, Category

def check_media_settings():
    """Проверка настроек медиа файлов"""
    print("=" * 60)
    print("ПРОВЕРКА НАСТРОЕК МЕДИА ФАЙЛОВ")
    print("=" * 60)
    
    # Проверка настроек
    print("\n📁 НАСТРОЙКИ:")
    print(f"  MEDIA_URL: '{settings.MEDIA_URL}'")
    print(f"  MEDIA_ROOT: '{settings.MEDIA_ROOT}'")
    print(f"  DEBUG: {settings.DEBUG}")
    
    # Проверка существования папки
    media_root = Path(settings.MEDIA_ROOT)
    print(f"\n📂 ПАПКА MEDIA_ROOT:")
    print(f"  Существует: {media_root.exists()}")
    if media_root.exists():
        print(f"  Путь: {media_root.absolute()}")
        print(f"  Это папка: {media_root.is_dir()}")
    
    # Проверка папки products
    products_dir = media_root / 'products'
    print(f"\n📦 ПАПКА PRODUCTS:")
    print(f"  Существует: {products_dir.exists()}")
    if products_dir.exists():
        print(f"  Путь: {products_dir.absolute()}")
        print(f"  Это папка: {products_dir.is_dir()}")
    
    # Проверка модели Product
    print(f"\n🖼️ МОДЕЛЬ PRODUCT:")
    image_field = Product._meta.get_field('image')
    print(f"  Поле image: {image_field}")
    print(f"  upload_to: '{image_field.upload_to}'")
    print(f"  blank: {image_field.blank}")
    print(f"  null: {image_field.null}")
    
    # Проверка товаров с изображениями
    products_with_images = Product.objects.filter(image__isnull=False)
    print(f"\n📊 ТОВАРЫ С ИЗОБРАЖЕНИЯМИ:")
    print(f"  Всего товаров: {Product.objects.count()}")
    print(f"  С изображениями: {products_with_images.count()}")
    
    if products_with_images.exists():
        print(f"  Примеры:")
        for product in products_with_images[:3]:
            print(f"    - {product.name}: {product.image.url}")
    
    # Проверка URL маршрутов
    print(f"\n🔗 URL МАРШРУТЫ:")
    print(f"  DEBUG режим: {settings.DEBUG}")
    if settings.DEBUG:
        print(f"  ✅ Медиа файлы доступны по URL: {settings.MEDIA_URL}")
        print(f"  📁 Физический путь: {settings.MEDIA_ROOT}")
    else:
        print(f"  ⚠️ В продакшене настройте веб-сервер для раздачи медиа файлов")
    
    print("\n✅ ПРОВЕРКА ЗАВЕРШЕНА!")
    print("=" * 60)

def test_image_upload():
    """Тестирование загрузки изображения"""
    print("\n🧪 ТЕСТИРОВАНИЕ ЗАГРУЗКИ ИЗОБРАЖЕНИЯ:")
    
    try:
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Создание тестового изображения
        image_content = b"fake_image_content"
        image = SimpleUploadedFile(
            "test_image.jpg",
            image_content,
            content_type="image/jpeg"
        )
        
        # Получение первой категории
        category = Category.objects.first()
        if not category:
            print("  ❌ Нет категорий в базе данных")
            return
        
        # Создание тестового товара
        product = Product.objects.create(
            name='Тестовый товар для проверки медиа',
            description='Описание тестового товара',
            category=category,
            price=100.00,
            image=image
        )
        
        print(f"  ✅ Создан тестовый товар: {product.name}")
        print(f"  📁 URL изображения: {product.image.url}")
        print(f"  📂 Физический путь: {product.image.path}")
        print(f"  📏 Размер файла: {product.image.size} байт")
        
        # Проверка существования файла
        if os.path.exists(product.image.path):
            print(f"  ✅ Файл существует на диске")
        else:
            print(f"  ❌ Файл не найден на диске")
        
        # Удаление тестового товара
        product.delete()
        print(f"  🗑️ Тестовый товар удален")
        
    except Exception as e:
        print(f"  ❌ Ошибка при тестировании: {e}")

if __name__ == "__main__":
    try:
        check_media_settings()
        test_image_upload()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("Убедитесь, что Django настроен корректно") 