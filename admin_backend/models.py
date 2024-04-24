from django.db import models
from account.models import DeveloperAdmin
from django.conf import settings 

# Create your models here.

Duration = (
    ("seven_days","Seven Days"),
    ("one_month","One Month"),
    ("four_month","Four Month"),
    ("six_month","Six Month"),
    ("tweleve_month","Twelve Month"),
    ("twentyfour_month","Twenty-Four Month")
)


# Create your models here.
      
class HotelUsers(models.Model):
    user = models.ForeignKey(DeveloperAdmin, on_delete=models.SET_DEFAULT, default=1, related_name='hotels')
    property_name = models.CharField(max_length=50,unique=True)
    owner_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    logo = models.ImageField(upload_to="logos/",null=True,blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    sales_executive = models.CharField(max_length=50,null=True)
    amount = models.BigIntegerField(null=True)
    tax = models.BigIntegerField(null=True)
    total_amount = models.BigIntegerField(null=True)
    duration = models.CharField(choices=Duration,max_length=100)
    website = models.URLField(max_length=200)
    agreement = models.ImageField(upload_to="agreements/",null=True,blank=True)
    qr_code = models.ImageField(upload_to="qr", null=True,blank=True)
    unique_url = models.CharField(max_length=255, unique=True,null=True)
    is_active = models.BooleanField(default=True) 
    
    
    def save(self, *args, **kwargs):
        self.user.is_hotel = True
        self.user.save()
        super(HotelUsers, self).save(*args, **kwargs)
        
        
    def __str__(self):
        return self.user.username