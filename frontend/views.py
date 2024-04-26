from django.shortcuts import render ,redirect
from hotel.models import *
from admin_backend .models import HotelUsers
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from accounts .model import DeveloperAdmin 

# Create your views here.

def menu_card(request, pk, username):
    # Retrieve hotel based on pk and username
    hotel_identifier = DeveloperAdmin.objects.filter(pk=pk, username=username).first()

    if hotel_identifier:
        # User is logged in and associated with a hotel
        menu_items = MenuItem.objects.filter(user_id=hotel_identifier)
        categories = Category.objects.filter(user_id=hotel_identifier)
        properties = HotelUsers.objects.filter(user_id=hotel_identifier)
        return render(request, 'frontend/menu_card.html', {'menu_items': menu_items, 'categories': categories,'properties':properties})
    else:
        # User is not logged in or not associated with a hotel (public access)
        menu_items = MenuItem.objects.all()
        categories = Category.objects.all()
        return render(request, 'frontend/public_menu_card.html', {'menu_items': menu_items, 'categories': categories})



# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')    
