from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

# Create your views here.

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Hello, world! This is the catalog index.")

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

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
        return super().form_valid(form)

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