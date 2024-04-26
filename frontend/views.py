from django.shortcuts import render ,redirect
from hotel.models import *
from admin_backend .models import HotelUsers
from django.shortcuts import get_object_or_404

# Create your views here.


def menu_card(request, pk, username):
    # Retrieve the HotelUsers object based on pk and username
    hotel_user = get_object_or_404(HotelUsers, id=pk, username=username)
    
    # Retrieve menu items and categories associated with the hotel_user
    menu_items = MenuItem.objects.filter(user_id=hotel_user.id)
    categories = Category.objects.filter(user_id=hotel_user.id)
    
    # Pass the retrieved items to the template
    return render(request, 'frontend/menu_card.html', {
        'menu_items': menu_items,
        'categories': categories,
        'hotel_user': hotel_user  # Optionally pass the hotel_user object to the template



# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')    
