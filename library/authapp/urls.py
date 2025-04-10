from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
    path('check-email/', views.check_email, name='check_email'),
    path('check-username/', views.check_username, name='check_username'),
]
