from django.db import models

# Create your models here.
class Menu(models.Model):
    item = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.item
    
    class Meta:
        indexes = [
            models.Index(fields=['item']),
        ]