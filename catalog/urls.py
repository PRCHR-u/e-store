from django.urls import path
from .views import HomeView, ContactsView, ProductDetailView, IndexView, ProductCreateView, ProductUpdateView, ProductDeleteView, CategoryProductsView

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('category/<int:category_id>/', CategoryProductsView.as_view(), name='category_products'),
]
