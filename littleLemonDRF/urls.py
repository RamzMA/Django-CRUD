from django.urls import path
from . import views

urlpatterns = [
    path('menu', views.menu, name="menu"),
    path('category/<int:pk>', views.category_detail, name='category_detail')
]