from django.urls import path
from .views import *
from . import views




urlpatterns =[
    
    
    path('hotel_index', hotel_index, name='hotel_index'),
    path('accounts/login/', login_view, name='admin_login'),     
    path('accounts/logout/', logout_view, name='admin_logout'),
    
    path('categories/', category_list, name='category_list'),
    path('menu_items/', menu_list, name='menu_list'),
    
    path('category/add', category_add, name='category_add'),
    path('category/<int:pk>/delete', category_delete, name='category_delete'),
    path('category/<int:pk>/edit', category_edit, name='category_edit'),
    
    
    path('menu_items/add', menu_items_add, name='menu_items_add'),
    path('menu_items/<int:pk>/delete', menu_items_delete, name='menu_items_delete'),
    path('menu_items/<int:pk>/edit', menu_items_edit, name='menu_items_edit'),
    
    
    path('toggle-availability/<int:pk>/', views.toggle_availability, name='toggle_availability'),

    
]