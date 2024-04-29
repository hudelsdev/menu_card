from django.shortcuts import render ,redirect
from hotel.models import *
from admin_backend .models import HotelUsers
from django.contrib.auth.decorators import login_required

# Create your views here.

def menu_card(request, pk, username):
    try:
        hotel = HotelUsers.objects.get(pk=pk, username=username)
    except HotelUsers.DoesNotExist:
        return render(request, '404.html', {'message': 'Hotel not found'})

    menu_items = MenuItem.objects.filter(user=hotel)
    categories = Category.objects.filter(user=hotel)
    properties = HotelUsers.objects.filter(pk=hotel.pk)  

    return render(request, 'frontend/menu_card.html', {'menu_items': menu_items, 'categories': categories,'properties': properties})



# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')    
