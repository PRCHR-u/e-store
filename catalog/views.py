from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product

# Create your views here.

def index(request):
    return HttpResponse("Hello, world! This is the catalog index.")

def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

def contacts(request):
    return render(request, 'catalog/contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})