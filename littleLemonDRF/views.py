from .models import Category
from .serializers import CategorySerializer
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

