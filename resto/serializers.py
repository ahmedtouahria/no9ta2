from rest_framework import serializers
from .models import Restaurant , Meal , SubscribeUser ,MealSubscribe

class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = ['id', 'name', 'price', 'photos', 'restaurant']
        
class RestoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = '__all__'
class SubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscribeUser
        fields = '__all__'
        extra_kwargs={'user':{'read_only':True}}
        
        
class MealSubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MealSubscribe
        fields = [ 'food', 'user', 'code', 'created_at']
        extra_kwargs={'code':{'read_only':True},'date':{'read_only':True},'user':{'read_only':True}}
        # function that returns the owner of a tweet
        