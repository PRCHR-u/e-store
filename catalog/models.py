from django.db import models
from django.conf import settings
from django.core.cache import cache

# Create your models here.

class CategoryManager(models.Manager):
    """Менеджер для категорий с кешированием"""
    
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

class Category(models.Model):
    """Модель категории товаров"""
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    objects = CategoryManager()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Переопределяем save для инвалидации кеша"""
        result = super().save(*args, **kwargs)
        # Инвалидируем кеши категорий
        cache.delete("all_categories")
        cache.delete("categories_with_count_published")
        cache.delete("categories_with_count_all")
        return result
    
    def delete(self, *args, **kwargs):
        """Переопределяем delete для инвалидации кеша"""
        result = super().delete(*args, **kwargs)
        # Инвалидируем кеши категорий
        cache.delete("all_categories")
        cache.delete("categories_with_count_published")
        cache.delete("categories_with_count_all")
        return result


class ProductManager(models.Manager):
    """Менеджер для продуктов с кешированием"""
    
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
    
    def get_product_by_id(self, product_id):
        """Получает продукт по ID с кешированием"""
        cache_key = f"product_by_id_{product_id}"
        cached_product = cache.get(cache_key)
        if cached_product is not None:
            return cached_product
        
        product = self.select_related('category', 'owner').get(id=product_id)
        cache.set(cache_key, product, 1800)  # 30 минут
        return product

class Product(models.Model):
    """Модель товара"""
    name = models.CharField(max_length=200, verbose_name='Наименование')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='Категория'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Цена за покупку'
    )
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        null=True, blank=True
    )

    objects = ProductManager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Переопределяем save для инвалидации кеша"""
        result = super().save(*args, **kwargs)
        # Инвалидируем кеши продуктов
        cache.delete("published_products")
        cache.delete(f"products_by_category_{self.category_id}_published")
        cache.delete(f"products_by_category_{self.category_id}_all")
        cache.delete(f"product_by_id_{self.id}")
        cache.delete(f"product_detail_{self.id}")
        return result
    
    def delete(self, *args, **kwargs):
        """Переопределяем delete для инвалидации кеша"""
        category_id = self.category_id
        product_id = self.id
        result = super().delete(*args, **kwargs)
        # Инвалидируем кеши продуктов
        cache.delete("published_products")
        cache.delete(f"products_by_category_{category_id}_published")
        cache.delete(f"products_by_category_{category_id}_all")
        cache.delete(f"product_by_id_{product_id}")
        cache.delete(f"product_detail_{product_id}")
        return result
