from django.urls import path
from . import views

"""
    categories: Leads to 127.0.0.1/8000/api/categories
    menu-items: Leads to 127.0.0.1/8000/api/menu-items
    menu-items<int:pk>: Leeds to 127.0.0.1/8000/api/menu-items/pk 
"""
urlpatterns = [
    path('categories', views.CategoryView.as_view(), name='categories'),
    path('menu-items', views.MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', views.SingleItemView.as_view(), name='menu-items-detail'),
    path('cart/menu-items', views.CartView.as_view(), name='cart'),
]
