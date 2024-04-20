from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, MenuItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.

def login_view(request):
    # If the user is already authenticated, redirect to hotel_index
    if request.user.is_authenticated:
        return redirect('hotel_index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('hotel_index')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'account/login.html')



def logout_view(request):
    logout(request)
    return redirect('admin_login')



@login_required
def hotel_index(request):
    if request.user.is_hotel:
        categories = Category.objects.filter(user=request.user)
        menuitems = MenuItem.objects.filter(user=request.user)
        properties = HotelUsers.objects.filter(user=request.user)
        return render(request, 'hotel/index.html', {'categories': categories, 'menuitems': menuitems,'properties': properties})
    else:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('admin_login')

    
# category & menu list

@login_required
def category_list(request):

    if request.user.is_hotel:
        categories = Category.objects.filter(user=request.user)
        page = request.GET.get('page', 1)
        paginator = Paginator(categories, 5)

        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)

        return render(request, 'hotel/category_list.html', {'categories': categories})
    else:
        return redirect('admin_login')

@login_required
def menu_list(request):
    if request.user.is_hotel:
        # Filter available menu items
        available_menu_items = MenuItem.objects.filter(user=request.user, available=True)

        # Filter finished menu items
        finished_menu_items = MenuItem.objects.filter(available=False)

        # Pagination for available menu items
        page = request.GET.get('page', 1)
        paginator = Paginator(available_menu_items, 5)

        try:
            menuitems = paginator.page(page)
        except PageNotAnInteger:
            menuitems = paginator.page(1)
        except EmptyPage:
            menuitems = paginator.page(paginator.num_pages)

        return render(request, 'hotel/menu_list.html', {'menuitems': menuitems, 'finished_menuitems': finished_menu_items})
    else:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('admin_login')



# category_view

@login_required
def category_add(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        Category.objects.create(
            user=user,
            name=name
        )
        return redirect('hotel_index')
    return render(request, 'hotel/add_category.html')

 
 
 
@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('hotel_index')
    return render(request, 'hotel/delete_category.html', {'category': category})



@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')

        category.name = name
        category.save()
        return redirect('hotel_index')

    return render(request, 'hotel/edit_category.html', {'category': category})



# menu_items_view



@login_required
def menu_items_add(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id, user=request.user)
        MenuItem.objects.create(
            user=user,
            name=name,
            category=category,
            price=price,
            description=description,
            image=image,
        )
        return redirect('hotel_index')

    categories = Category.objects.filter(user=request.user)
    return render(request, 'hotel/add_menu_items.html', {'categories': categories})



def menu_items_delete(request, pk):
    menu_items = get_object_or_404(MenuItem, pk=pk)

    if request.method == 'POST':
        menu_items.delete()
        return redirect('hotel_index')
    return render(request, 'hotel/delete_menu_items.html', {'menu_items': menu_items})


def menu_items_edit(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    category = categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category') 
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        category = get_object_or_404(Category, pk=category_id)
        
        if image:
            menu_item.image = image
        menu_item.name = name
        menu_item.category = category  
        menu_item.price = price
        menu_item.description = description
        menu_item.save()
        return redirect('hotel_index')

    return render(request, 'hotel/edit_menu_items.html', {'menu_item': menu_item,'categories': categories})




# availability 

def toggle_availability(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    menu_item.available = not menu_item.available
    menu_item.save()
    return redirect('menu_list')  


