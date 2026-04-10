from rest_framework import serializers
from .models import Category, MenuItem

#Category serializer
"""
    Meta: Configuring serializer
    model: Setting model for mapping for serializer, so database knows where to read/write
    fields: Fields from model that we want to expose
"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


#MenuItem Serializer
"""
    category: This ensures that when user GET request, instead of category id:1 it nests all information related to object
    category_id: This does the opposite it ensures it is only able to be written in, wont show up in GET response
"""
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_id']