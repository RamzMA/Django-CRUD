from django.urls import path
from .models import views

urlpatterns = [
    path('ratings', views.RatingsView.as_view()),
]