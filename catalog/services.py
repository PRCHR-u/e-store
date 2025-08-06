from django.shortcuts import get_object_or_404
from django.db import models
from django.core.cache import cache
from .models import Category, Product


def get_all_products(only_published=True):
    """
    Сервисная функция для получения всех продуктов
    
    Args:
        only_published (bool): Возвращать только опубликованные продукты
    
    Returns:
        QuerySet: Список всех продуктов
    """
    if only_published:
        # Используем низкоуровневое кеширование через менеджер
        return Product.objects.get_published_products()
    else:
        # Для всех продуктов (включая неопубликованные) используем прямой запрос
        return Product.objects.select_related('category', 'owner').order_by('-created_at')


def get_products_by_category(category_id=None, category_slug=None, only_published=True):
    """
    Сервисная функция для получения списка продуктов по категории
    
    Args:
        category_id (int, optional): ID категории
        category_slug (str, optional): Slug категории
        only_published (bool): Возвращать только опубликованные продукты
    
    Returns:
        QuerySet: Список продуктов в указанной категории
    """
    if category_id:
        # Используем низкоуровневое кеширование через менеджер
        return Product.objects.get_products_by_category(category_id, only_published)
    elif category_slug:
        # Для slug используем старый метод
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.get_products_by_category(category.id, only_published)
    else:
        raise ValueError("Необходимо указать category_id или category_slug")


def get_products_by_owner(owner_id, only_published=True):
    """
    Сервисная функция для получения продуктов по владельцу
    
    Args:
        owner_id (int): ID владельца
        only_published (bool): Возвращать только опубликованные продукты
    
    Returns:
        QuerySet: Список продуктов владельца
    """
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
    """
    Сервисная функция для получения продуктов по диапазону цен
    
    Args:
        min_price (decimal, optional): Минимальная цена
        max_price (decimal, optional): Максимальная цена
        only_published (bool): Возвращать только опубликованные продукты
    
    Returns:
        QuerySet: Список продуктов в указанном диапазоне цен
    """
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
    """
    Сервисная функция для получения всех категорий с количеством продуктов
    
    Args:
        only_published (bool): Учитывать только опубликованные продукты
    
    Returns:
        QuerySet: Список категорий с аннотацией количества продуктов
    """
    # Используем низкоуровневое кеширование через менеджер
    return Category.objects.get_categories_with_products_count(only_published)


def invalidate_products_cache(category_id=None, product_id=None):
    """
    Инвалидирует кеш продуктов при изменении данных
    
    Args:
        category_id (int, optional): ID категории для инвалидации конкретного кеша
        product_id (int, optional): ID продукта для инвалидации кеша детальной страницы
    """
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


def invalidate_all_products_cache():
    """
    Инвалидирует все кеши, связанные с продуктами
    """
    # Получаем все категории и инвалидируем их кеши
    categories = Category.objects.all()
    for category in categories:
        invalidate_products_cache(category.id)
    
    # Инвалидируем общие кеши категорий
    cache.delete("categories_with_products_published")
    cache.delete("categories_with_products_all") 