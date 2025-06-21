from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product
from django.views.generic import View, TemplateView, ListView, DetailView

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