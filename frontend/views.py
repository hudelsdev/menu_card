from django.shortcuts import render ,redirect
from hotel.models import *
from admin_backend .models import HotelUsers
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Create your views here.

def menu_card(request, pk, username):
    # Retrieve hotel user based on the username in the URL
    hotel_user = get_object_or_404(HotelUsers, username=username)

    # Filter menu items and categories for the specific hotel
    menu_items = MenuItem.objects.filter(user_id=hotel_user.id)
    categories = Category.objects.filter(user_id=hotel_user.id)
    
    # Pass the retrieved data to the template
    return render(request, 'frontend/menu_card.html', {'menu_items': menu_items, 'categories': categories, 'hotel_user': hotel_user})




# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')    
