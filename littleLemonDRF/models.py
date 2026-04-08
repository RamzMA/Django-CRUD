from django.db import models

# Create your models here.


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

class Menu(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    catgeory = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)