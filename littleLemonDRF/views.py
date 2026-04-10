from .models import Category, MenuItem, Cart
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

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

#Cart View
"""
    permission_classes: As we only need user to be logged in to get their cart and delete from their cart
    get_queryset: As instead of Cart.objects.all() which gets all carts which is a security risk
        - We filter for user=self.request.user which is the current user making the request
    delete: This filters for the user making the request and deletes the cart
        -returns response and status code
"""
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({'Message': 'Cart Cleared'}, status=200)
    