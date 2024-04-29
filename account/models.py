from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class DeveloperAdmin(AbstractUser):
    is_admin_user = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)
    is_hotel = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.username
