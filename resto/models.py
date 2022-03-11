from django.db import models
from django.core.validators import RegexValidator
import random
import os
from user.models import User
from .utils import generate_random_code
from django.conf import settings
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")

    
def upload_image_path_resto(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "resto/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )
     
class Restaurant(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name     = models.CharField(max_length=200,unique=True,blank=False,null=False)
    position = models.CharField(max_length=200,blank=False,null=False)
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    email = models.EmailField(max_length=254)
    image = models.ImageField(upload_to=upload_image_path_resto)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name
"""
functions upload_image_path_profile() and get_filename_ext() 
to generate image path to the server 
"""

def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "meals/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )
    
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


class Meal(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    photos=models.ImageField(upload_to=upload_image_path_profile)
    created_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} - {self.price} $"


class SubscribeUser(models.Model):
    type_choice = [
        (89, 89),
        (130, 130),
        (220, 220),
    ]
    type_sub = models.IntegerField(choices=type_choice,default=89)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)     
    def __str__(self):
        return str(self.user)
 
class MealSubscribe(models.Model):
    food = models.ForeignKey(Meal,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    code = models.CharField(max_length=10,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    resto=models.ForeignKey(Restaurant,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"{self.user} - {self.code} -{str(self.created_at)[:10]}"
    
    def save(self, *args, **kwargs):
       if self.code=='':
           code = generate_random_code()
           self.code=code
       super().save(*args, **kwargs)