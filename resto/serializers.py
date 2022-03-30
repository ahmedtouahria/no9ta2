from rest_framework import serializers

from user.models import User
from .models import Restaurant , Meal , SubscribeUser ,MealSubscribe

class MealSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(),)
    class Meta:
        model = Meal
        fields = ['id', 'name', 'price', 'photos', 'restaurant','resto_name','isAvailaible']
    
class RestoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),)
    class Meta:
        model = Restaurant
        fields = ['id', 'name','user', 'user_name', 'phone', 'image','active','position','latitude','longitude',]
class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscribeUser
        fields = '__all__'
        extra_kwargs={'user':{'read_only':True}}
        
        
class MealSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealSubscribe
        fields = [ 'food','food_name', 'user','user_name', 'code', 'created_at']
        extra_kwargs={'code':{'read_only':True},'date':{'read_only':True},'user':{'read_only':True}}
        # function that returns the owner of a tweet
        