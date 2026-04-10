from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

"""
    Generics: allows for prebuilt GET,POST,EDIT,DELETE with LIST,CREATE,UPDATE,DELETE view
    IsAdmin: Built in function to check if user is user.staff
    IsAuthenticated: Built in function to check if user is logged in
    Queryset: Tells view what data to work with, for instance Category.objects.all() is all fields of category. Used for GET response.
    Serializer_class: Tells view what serializer to use to convert data to and from json
"""
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
#MenuItem View
"""
    Ordering_fields: Ensures order is able to be sorted by price (e.g. /api/menu-items?ordering=price)
    search_fields: Ensures order is able to be searched (e.g. /api/menu-items?search=pizza)
"""
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    search_fields = ['title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

#SingleItem View
"""
    RetrieveUpdateDestroyAPIView: Gets, updates and deletes
"""
class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminUser()]
