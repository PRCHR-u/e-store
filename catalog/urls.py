from django.urls import path
from .views import HomeView, ContactsView, ProductDetailView, IndexView

urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
