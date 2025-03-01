# from django.db import models

# Create your models here.

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    price = models.IntegerField()
    
    def __str__(self):
        return self.title