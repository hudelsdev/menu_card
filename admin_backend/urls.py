from django.urls import path, include
from .views import *



urlpatterns = [
     path('admin_home/', admin_home, name='admin_home'),
     path('accounts/super_admin_login/', super_admin_login, name='super_admin_login'),
     path('accounts/super_admin/logout/', super_admin_logout, name='super_admin_logout'),
     path('admin_property_list/', property_list, name='property_list'),
     path('admin_property/<int:pk>/detail', property_detail, name='property_detail'),
     path('admin_property_create/', property_create, name='property_create'),
     path('admin_property/<int:pk>/edit', property_edit, name='property_edit'),
     path('admin_property/<int:pk>/delete', property_delete, name='property_delete'),
     path('admin_property/<int:pk>/property_deactivate', property_deactivate, name='property_deactivate'),
     path('admin_property/<int:pk>/property_activate', property_activate, name='property_activate'),
]