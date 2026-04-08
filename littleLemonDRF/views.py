from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Menu, Category
from .serializers import MenuItemSerializer, CategorySerializer
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

# Create your views here.
@csrf_exempt
def menu(request):
    if request.method == 'GET':
        menu = Menu.objects.all().values()
        return JsonResponse({'menu': list(menu)})
    elif request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')

        menu = Menu(title=title,description=description,price=price)

        try:
            menu.save()
        except IntegrityError:
            return JsonResponse({'error': 'true', 'message': 'required field missing'}, status=400)
        
        return JsonResponse(model_to_dict(menu), status=201)
    
@api_view()
def category_detail(request,pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)
