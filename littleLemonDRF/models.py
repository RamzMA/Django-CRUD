from django.db import models

# Catgeory class
"""
    Slug: URL-friendly version of a name, only allows letters, numbers, hyphens and underscores.
        - example of slug would be /api/menu-items?category=main-course
        -compared to /api/categories/1
    Title: Title of category
"""
class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)

    #Easily readable
    def __str__(self):
        return self.title


#MenuItem class

"""
    db_index: Allows for faster searching with unique values in the database such as title
    decimal_places: How many numbers after decimal (e.g. 12.12) is 2 decimal places
    max_digits: how many digits in the number (e.g. 123.23) is 5 digits so max_digits is 5
    
    category: Foreign key that relates to model:Category
        -On delete it is models.PROTECT which ensures no category can be deleted if it has menu items
"""
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.title