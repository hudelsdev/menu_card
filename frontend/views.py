from django.shortcuts import render ,redirect
from hotel.models import *
from admin_backend .models import HotelUsers

# Create your views here.


def menu_card(request):
    hotel_identifier = request.user.id
    menu_items = MenuItem.objects.filter(user_id=hotel_identifier)
    categories = Category.objects.filter(user_id=hotel_identifier)
    properties = HotelUsers.objects.filter(user_id=hotel_identifier)
    return render(request, 'frontend/menu_card.html', {'menu_items': menu_items, 'categories': categories,'properties':properties})



# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')    