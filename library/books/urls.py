from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('new/', views.add_book, name='add_book'),
    path('<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('create_order/', views.create_order, name='create_order'),
    path('orders/', views.orders, name='orders'),
]

