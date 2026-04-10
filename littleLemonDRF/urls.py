from django.urls import path
from . import views

urlpatterns = [
    path('categories', views.CategoryView.as_view(), name='categories'),
    
]
