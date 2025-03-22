from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Админ'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
    
