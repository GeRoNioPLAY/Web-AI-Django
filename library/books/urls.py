from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list'),
    path('new/', views.add_book, name='add_book'),
    path('<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('<int:pk>/delete/', views.delete_book, name='delete_book'),
]

