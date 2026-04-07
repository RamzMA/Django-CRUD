from django.shortcuts import render
from .models import Menu
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