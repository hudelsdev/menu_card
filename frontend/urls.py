from django.urls import path, include
from .views import *
from . import views


urlpatterns = [
     path('hotel/<int:user_id>-menu/', menu_card, name='menu_card'),
    path('toggle-availability/<int:pk>/', views.toggle_availability, name='toggle_availability'),
]
