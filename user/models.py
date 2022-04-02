from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator  
from .utils import generate_random_code
import random
import os

# using a custom user from override django authentication model USER
class UserManager(BaseUserManager):
    def create_user(self, name, phone,country, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')
        if not name:
            raise ValueError('user must have a name')
        if not country:
            raise ValueError('user must have a country')
        user_obj = self.model(
            name=name,
            phone=phone,
            country=country,
            password=password
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, name, phone,country, password=None):
        user = self.create_user(
            name,
            phone,country,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self,name, phone,country, password=None):
        user = self.create_user(
            name,
            phone,
            country,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user
class User(AbstractBaseUser,PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    name = models.CharField(max_length=20, blank=False, null=False,unique=True)
    password=models.CharField(max_length=100, blank=False, null=False,validators=[MinLengthValidator(8)])
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_resto=models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    country = CountryField()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name','country']
    created_at=models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    def __str__(self):
        return self.name
    def get_country(self):
        return str(self.country)
    def get_full_name(self):
        return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):

        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1, 9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_image_path_profile, default=None, null=True, blank=True)
    code = models.CharField(max_length=12,blank=True)
    recommended_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True,related_name='ref_by')
    isPartner = models.BooleanField(default=False)
    profit=models.FloatField(default=0.0)
    def __str__(self):
        return str(self.user)
    def country(self):
        return self.user.country
    def num_of_partner(self):
        partners = Profile.objects.filter(isPartner=True)
        return len(partners)       
        
        
    def save(self, *args, **kwargs):
       if self.code=='':
           code = generate_random_code()
           self.code=code
       super().save(*args, **kwargs) # Call the real save() method

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


post_save.connect(user_created_receiver, sender=User)
