from cProfile import label
from django import forms

from resto.models import Meal, Restaurant
from user.models import User
class MealForm(forms.ModelForm):
    class  Meta:
     model = Meal
     fields = [
         'name',
         'price',
         'photos',
         'description',
         'isAvailaible'
     ]
     widgets={
         'name':forms.TextInput(attrs={'class':'form-control w-75 '}),
         'price':forms.NumberInput(attrs={'class':'form-control w-75 '}),
         'photos':forms.FileInput(attrs={'class':'form-control w-75 '}),
         'description':forms.TextInput(attrs={'class':'form-control w-75 mt-1 '}),
         'isAvailaible':forms.CheckboxInput()
         
     }
     labels = {
            'name': 'إسم الوجبة ',
            'price':'السعر ',
            'photos':'صورة الوجبة ' ,
            'description':'وصف الوجبة ' ,
            'isAvailaible':'متاحة'
        }
class RegisterForm(forms.ModelForm):
    class  Meta:
     model = User
     fields = [
         'name',
         'phone',
         'password',
     ]
     widgets={
         'name':forms.TextInput(attrs={'class':'form-control w-100 my-2 '}),
         'phone':forms.TextInput(attrs={'class':'form-control w-100 my-2 '}),
         'password':forms.PasswordInput(attrs={'class':'form-control w-100 my-2 '}),
         
     }    
     labels = {
            'name': 'إسم المطعم ',
            'phone':'رقم الهاتف',
            'password':'كلمة السر'
        }
class CreateResto(forms.ModelForm):
    class  Meta:
     model = Restaurant
     fields = [
         'latitude',
         'longitude',
         'image',
     ]
     widgets={
         'latitude':forms.TextInput(attrs={'class':'form-control w-100 my-2 ','id':'latitude','readonly':'true'}),
         'longitude':forms.TextInput(attrs={'class':'form-control w-100 my-2 ','id':'longitude','readonly':'true'}),
         'image':forms.FileInput(attrs={'class':'my-2 '}),
         
     }  
     labels = {
            'latitude': 'إحداثية أ ',
            'longitude':'إحداثية ب',
            'image':' صورة المطعم'
        }  

class LoginForm(forms.ModelForm):
    class  Meta:
     model = User
     fields = [
         'phone',
         'password',
     ]
     widgets={
         'phone':forms.TextInput(attrs={'class':'form-control w-100 my-2 '}),
         'password':forms.PasswordInput(attrs={'class':'form-control w-100 my-2 '}),
         
     }    
     labels = {
            'phone':'رقم الهاتف',
            'password':'كلمة السر'
        }
     