from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('products/', views.list_products),
    path('products/<int:id>/', views.get_product),
    path('products/create/', views.create_product),
    path('products/<int:id>/update/', views.update_product),
    path('products/<int:id>/delete/', views.delete_product),
]