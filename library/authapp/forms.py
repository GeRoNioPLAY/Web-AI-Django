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

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='Имя пользователя')
    email = forms.EmailField(label='Электронная почта')
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')