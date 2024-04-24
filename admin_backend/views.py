from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login,logout,get_user_model
from django.contrib import messages
from account.models import DeveloperAdmin 
from .models import Duration ,HotelUsers
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



User = get_user_model()


@login_required
def admin_home(request):
    if request.user.is_superuser:
        properties = HotelUsers.objects.all()
        search_query = request.GET.get('q')
        if search_query:
            properties = properties.filter(property_name__icontains=search_query)
            
        registered_hotels_count = HotelUsers.objects.count()
        return render(request, 'admin/admin_index.html', {'properties': properties,'registered_hotels_count': registered_hotels_count})
    else:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('super_admin_login')
    
      


def super_admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login Success")
            return redirect('admin_home')
        else:
            messages.error(request, "Invalid username or password")
    
    
    if request.user.is_authenticated:
        return redirect('admin_home')

    return render(request, 'admin/super_admin_login.html')



def super_admin_logout(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect('super_admin_login')  



def property_list(request):
    properties = HotelUsers.objects.all()
    active_properties = HotelUsers.objects.filter(is_active=True)
    inactive_properties = HotelUsers.objects.filter(is_active=False)
    return render(request, 'admin/property_list.html', {'properties': properties,'active_properties': active_properties, 'inactive_properties': inactive_properties})


def property_detail(request, pk):
    property = get_object_or_404(HotelUsers, pk=pk)
    return render(request, 'admin/property_detail.html', {'property': property})



def property_create(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            property_name = request.POST.get('property_name')
            owner_name = request.POST.get('owner_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            logo = request.FILES.get('logo')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            sales_executive = request.POST.get('sales_executive')
            amount = request.POST.get('amount')
            tax = request.POST.get('tax')
            total_amount = request.POST.get('total_amount')
            duration = request.POST.get('duration')
            website = request.POST.get('website')
            agreement = request.FILES.get('agreement')
            qr_code = request.FILES.get('qr_code')

            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')
                
                if password != confirm_password:
                    messages.error(request, "Passwords do not match.")
                    return redirect('property_create')
                
                user = User.objects.create_user(username=username, password=password)
                
                

                hotel_user = user.hotels.create(
                    property_name=property_name,
                    owner_name=owner_name,
                    email=email,
                    mobile=mobile,
                    logo=logo,
                    address=address,
                    city=city,
                    state=state,
                    sales_executive=sales_executive,
                    amount=amount,
                    tax=tax,
                    total_amount=total_amount,
                    duration=duration,
                    website=website,
                    agreement=agreement,
                    qr_code=qr_code,
                )
                
                 # Generate unique URL based on user ID and username
                 
                unique_url = f"https://127.0.0.1/hotel/{hotel_user.id}-{username.lower().replace(' ', '-')}"
                hotel_user.unique_url = unique_url
                hotel_user.save()   

                messages.success(request, f"Property created successfully. Unique URL: {unique_url}")
                print(reverse('admin_home'))
                return HttpResponseRedirect(reverse('admin_home'))
            except IntegrityError as e:
                if 'unique constraint' in str(e) and 'username' in str(e):
                    messages.error(request, "Username already exists. Please choose a different username.")
                else:
                    messages.error(request, "Failed to create property. Please ensure all fields are valid.")
        else:
            messages.error(request, "You don't have permission to create properties.")
            
      # Retrieve user_id here
    user_id = request.user.id       
    duration_choices = Duration  
    return render(request, 'admin/property_create.html', {'duration_choices': duration_choices,'user_id': user_id})




def property_edit(request, pk):
    property = get_object_or_404(HotelUsers, pk=pk)
    if request.method == 'POST':
        if request.user.is_superuser:     
            
            property.property_name = request.POST.get('property_name')
            property.owner_name = request.POST.get('owner_name')
            property.email = request.POST.get('email')
            property.mobile = request.POST.get('mobile')
            property.logo = request.FILES.get('logo')
            property.address = request.POST.get('address')
            property.city = request.POST.get('city')
            property.state = request.POST.get('state')
            property.sales_executive = request.POST.get('sales_exceutive')
            property.amount = request.POST.get('amount')
            property.tax = request.POST.get('tax')
            property.total_amount = request.POST.get('total_amount')
            property.duration = request.POST.get('duration')
            property.website = request.POST.get('website')
            property.agreement = request.FILES.get('agreement')
            property.qr_code = request.FILES.get('qr_code')
            
            property.save()
            return redirect('property_detail', pk=property.pk)
        else:
            return HttpResponseForbidden("You don't have permission to edit this property.")
    return render(request, 'property_edit.html', {'property': property})

def property_delete(request, pk):   
    property = get_object_or_404(HotelUsers, pk=pk)
    if request.method == 'POST':
        if request.user.is_superuser:  
            property.delete()
            return redirect('property_list')
        else:
            return HttpResponseForbidden("You don't have permission to delete this property.")
    return render(request, 'property_delete.html', {'property': property})



# views.py

def property_deactivate(request, pk):
    property = get_object_or_404(HotelUsers, pk=pk)
    user = property.user
    if request.method == 'POST':
        if request.user.is_superuser:  
            property.is_active = False
            property.save()
            user.is_active = False
            user.save()
            messages.success(request, "Property and associated user deactivated successfully.")
            return redirect('admin_home')
        else:
            return HttpResponseForbidden("You don't have permission to deactivate this property.")
    return render(request, 'property_deactivate.html', {'property': property})





def property_activate(request, pk):
    property = get_object_or_404(HotelUsers, pk=pk)
    user = property.user
    if request.method == 'POST':
        if request.user.is_superuser: 
            property.is_active = True
            property.save()
            user.is_active = True
            user.save()
            messages.success(request, "Property and associated user activated successfully.")
            return redirect('admin_home')
        else:
            return HttpResponseForbidden("You don't have permission to activate this property.")
    return render(request, 'property_activate.html', {'property': property})




# def generate_unique_url(request):
#     if request.method == 'GET':
#         username = request.GET.get('username')
#         hotel_id = request.GET.get('hotel_id')  
        
#         if username and hotel_id:
#             domain = request.get_host()
#             unique_url = f"{domain}/{hotel_id}-{username}"
            
#             return HttpResponseRedirect(reverse('username') + f'?unique_url={unique_url}')
#         else:
#             return JsonResponse({'error': 'Username and hotel ID are required'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)