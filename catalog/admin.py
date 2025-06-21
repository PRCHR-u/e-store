from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для модели Category"""
    list_display = ['id', 'name']
    search_fields = ['name', 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для модели Product"""
    list_display = ['id', 'name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name', 'description']
    list_select_related = ['category']
