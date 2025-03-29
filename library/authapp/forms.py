from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True, label="Почта")

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

class UserLogin(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "password")

class UserDataChange(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
