from rest_framework import serializers
from django.contrib.auth import authenticate
from django_countries.serializers import CountryFieldMixin
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'phone')


class CreateUserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'phone', 'country', 'password')
        password = serializers.CharField(
            style={'input_type': 'password'}, min_length=8, max_length=100, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'country')

   
class LoginUserSerializer(CountryFieldMixin,serializers.Serializer):
    class Meta: 
        model = User
        fields = ('id', 'phone', 'name', 'country')
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get('request'),
                                    phone=phone, password=password)

            else:
                msg = {'detail': 'Phone number is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Used for both password change (Login required) and 
    password reset(No login required but otp required)
    not using modelserializer as this serializer will be used for for two apis
    """

    password_1 = serializers.CharField(required=True)
    # password_1 can be old password or new password
    password_2 = serializers.CharField(required=True)
    # password_2 can be new password or confirm password according to apiview
 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'image','code','city','recommended_by','num_of_partner']
        extra_kwargs={'recommended_by':{'read_only':True},'code':{'read_only':True}}