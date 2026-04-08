from rest_framework import serializers
from decimal import Decimal
from .models import Menu, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = serializers.HyperlinkedRelatedField(
        queryset = Category.objects.all(),
        view_name = 'category_detail'
    )

    class Meta:
        model = Menu
        fields = ['id','title', 'description','price', 'price_after_tax','category']

    def calculate_tax(self, product:Menu):
        return product.price * Decimal(1.1)
