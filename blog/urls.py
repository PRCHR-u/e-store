from django.urls import path
from .views import BlogPostListView, BlogPostDetailView, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('post/<int:pk>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('post/create/', BlogPostCreateView.as_view(), name='blog_create'),
    path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='blog_edit'),
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),
] 