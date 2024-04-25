from django.shortcuts import render ,redirect
from hotel.models import *
from admin_backend .models import HotelUsers
from django.shortcuts import get_object_or_404

# Create your views here.


def menu_card(request, pk, username):
    hotel_user = get_object_or_404(HotelUsers, id=pk)

    menu_items = MenuItem.objects.filter(user_id=hotel_user.id)
    categories = Category.objects.filter(user_id=hotel_user.id)
    properties = Category.objects.filter(user_id=hotel_user.id)
    
    return render(request, 'frontend/menu_card.html', {'menu_items': menu_items, 'categories': categories, 'hotel_user': hotel_user,'properties':properties})



# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')    
