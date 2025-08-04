from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services import get_products_by_category, get_all_categories_with_products, invalidate_products_cache

# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, world! This is the catalog index.")

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        # Используем низкоуровневое кеширование через менеджер
        return Product.objects.get_published_products()

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        # Кеширование на уровне представления
        cache_key = f"product_detail_{self.kwargs.get('pk')}"
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return cached_response
        
        response = super().get(request, *args, **kwargs)
        # Кешируем на 15 минут
        cache.set(cache_key, response, 60 * 15)
        return response

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        result = super().form_valid(form)
        # Инвалидируем кеш после создания продукта
        invalidate_products_cache()
        return result

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.groups.filter(name='Модератор продуктов').exists():
            return HttpResponse('Редактирование разрешено только владельцу или модератору.', status=403)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Проверка права на отмену публикации
        if 'is_published' in form.changed_data and not form.cleaned_data['is_published']:
            if not self.request.user.has_perm('catalog.can_unpublish_product'):
                form.add_error('is_published', 'У вас нет права отменять публикацию.')
                return self.form_invalid(form)
        result = super().form_valid(form)
        # Инвалидируем кеш после обновления продукта
        invalidate_products_cache(product_id=form.instance.id)
        return result

@method_decorator(permission_required('catalog.delete_product', raise_exception=True), name='dispatch')
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_moderator = request.user.groups.filter(name='Модератор продуктов').exists()
        if obj.owner != request.user and not is_moderator:
            return HttpResponse('Удаление разрешено только владельцу или модератору.', status=403)
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        product_id = self.get_object().id
        result = super().delete(request, *args, **kwargs)
        # Инвалидируем кеш после удаления продукта
        invalidate_products_cache(product_id=product_id)
        return result


class CategoryProductsView(ListView):
    """Представление для отображения продуктов по категории"""
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return get_products_by_category(category_id=category_id, only_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        from .models import Category
        context['category'] = get_object_or_404(Category, id=category_id)
        # Используем кешированные категории из контекстного процессора
        context['categories'] = get_all_categories_with_products()
        return context