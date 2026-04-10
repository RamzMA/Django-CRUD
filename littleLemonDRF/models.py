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
