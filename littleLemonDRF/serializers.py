from rest_framework import serializers
from .models import Category, MenuItem, Cart

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


#Cart Serializer
"""
    user: HiddenField ensures never sends ID, user is set to whoever is making request
    super().create(validated_data): Calls parent method to save data to database
"""
class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_menuitem_id(self, value):
        try:
            MenuItem.objects.get(pk=value)
        except MenuItem.DoesNotExist:
            raise serializers.ValidationError("Menu Item does not exist!")
        return value
    
    def create(self, validated_data):
        menuitem = MenuItem.objects.get(pk=validated_data['menuitem_id'])
        validated_data['unit_price'] = menuitem.price
        validated_data['price'] = menuitem.price * validated_data['quantity']
        validated_data['menuitem'] = menuitem
        return super().create(validated_data)