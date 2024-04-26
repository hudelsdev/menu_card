from django.shortcuts import render ,redirect
from hotel.models import *
from admin_backend .models import HotelUsers
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.

def menu_card(request, pk, username):
    # Retrieve the hotel user (DeveloperAdmin) using the provided pk
    hotel_user = get_object_or_404(DeveloperAdmin, pk=pk)

    # Filter categories and menu items associated with the hotel user
    categories = Category.objects.filter(user=hotel_user)
    menu_items = MenuItem.objects.filter(user=hotel_user)

    # Pass the categories and menu items to the template
    context = {
        'categories': categories,
        'menu_items': menu_items,
        'hotel_user': hotel_user  
    }

    return render(request, 'frontend/menu_card.html', context)




# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')    
