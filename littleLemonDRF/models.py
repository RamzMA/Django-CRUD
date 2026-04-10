from django.db import models
from django.contrib.auth.models import User

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
    
#Cart class
"""
    user: Built in user model for authentification, when user is deleted
        -models.CASCADE as if user is gone their cart should be gone too
    menuitem: Foreign key relating to menuitem, when user is gone menuitem in cart should be gone too
    quantity: Uses SmallIntegerField as it goes up to 32k and no one needs that much items unless ur shaq
    unit_price: Stores price of item when added to cart incase price is later increased, keeping original price
    price: For unit_price * quantity 
    Meta unique_together: Ensures when adding same item 2 times per user it increases quantity and doesnt add item seperately 2 times
"""
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('user', 'menuitem')

    def __str__(self):
        return f"{self.user.username} - {self.menuitem.title}"
    
#Order class
"""
    user: If user is deleted delete order aswell, therefore CASCADE
    delivery_crew: Due to user already being a foreign key assigned to User
        -You must implement related_name to distinguish 
        -on_delete=models.SET_NULL: Does not delete order instead sets to null, null by default
    date: The date, self explanitory 
"""
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='delivery_crew'
    )
    status = models.BooleanField(default=False, db_index=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

#Order Item class
"""
    unique_together: Like before, means that same menuitem cannot apprear 2 times in order seperately
"""
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('order', 'menuitem')

    def __str__(self):
        return f"{self.menuitem.title} In Order {self.order.id}"
