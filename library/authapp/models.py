import bcrypt
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


# class CustomUser(AbstractUser):
#     ROLE_CHOICES = (
#         ('user', 'Пользователь'),
#         ('admin', 'Админ'),
#     )

#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

#     def __str__(self):
#         return self.username

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='user'):
        if not email:
            raise ValueError('Нужно ввести почту')
        if not username:
            raise ValueError('Нужно ввести имяпользователя')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
        )

        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, role='admin'):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, choices=[('user', 'User'), ('admin', 'Admin')], default='user')
    password_hash = models.CharField(max_length=128, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    def set_password(self, raw_password):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), salt)
        self.password_hash = hashed.decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash.encode('utf-8'))