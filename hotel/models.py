from django.db import models
from admin_backend .models import HotelUsers
from account .models import DeveloperAdmin

# Create your models here.

    
    
    
class Category(models.Model):
    user = models.ForeignKey(DeveloperAdmin, on_delete=models.CASCADE,null=True,related_name='hotel_categories')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


    

class MenuItem(models.Model):
    user = models.ForeignKey(DeveloperAdmin, on_delete=models.CASCADE,null=True, related_name='hotel_menus') 
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="dishes/",null=True,blank=True)
    available = models.BooleanField(default=True) 
    
    def __str__(self):
        return self.name
