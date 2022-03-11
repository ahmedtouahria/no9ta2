from rest_framework.response import Response
from rest_framework import  generics
from resto.models import Restaurant
from user.models import User,Profile
from .serializers import CreateUserSerializer, LoginUserSerializer ,ProfileSerializer
from knox.models import AuthToken
from django.contrib.auth import login
#from rest_framework.authtoken.serializers import AuthTokenSerializer
#from rest_framework.authentication import TokenAuthentication
from .custompermission import IsOwnerOrReadOnly
from knox.views import LoginView as KnoxLoginView
from rest_framework import response, status, permissions
#from django.contrib.auth import authenticate
#  first create endpoints for authenticated user

"""
Now I will write two Classes to register the user

Class 1:-----> with referal link 
**When the user registers using the invite link, the link will be provided with a code
**The code was previously recorded in Profile Class
**Each user has his own code
"""
#----------- With a Referal Link-----------------#
class RegisterUserAPIView(generics.GenericAPIView):
    # We receive data from serializer for JSON format
    serializer_class = CreateUserSerializer
    # Now , override Function post for sending data to server
    def post(self, request, *args, **kwargs):
        # get Code from url ---> exemple : www.exemple.com/register/he105kop
        #code = he105kop
        try:
          code = str(kwargs.get('ref_code'))
          # get  user Profile id 
          profile = Profile.objects.get(code=code)
          # create a session 'ref_profile' 
          request.session['ref_profile'] = profile.id
          profile.isPartner=True
          profile.profit+=1.5
          profile.save()
          #print('id', profile.isPartner)
        except :  
         pass
        
#generics class has already function "get_serializer(data=...)" to assign data from user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
       # print('namooooooo',user.name)
        
        # get session key from request['ref_link']
        profile_id=request.session['ref_profile']
       # print(profile_id)
        # testing if profile it exist
        if profile_id is not None:
            #Now , We got the profile 
            recommended_by_profile = Profile.objects.get(id=profile_id)
            #And since the user class is related to it ->'Profile' 
            # We get the user ;)
            registered_user = User.objects.get(id=user.id)
            registered_profile = Profile.objects.get(user=registered_user)
            #Then we assign the user who recommended it
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.save()
        else:
            print('profile_id is none')    
        print(request.session.get_expiry_date())
        return Response({
        "user": CreateUserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1],
        })          


####################################################################
"""
Class 2:-----> without referal link 
**
When the user register with normal link --> www.exemple.com/register 

"""
class RegisterUserWithOutSession(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
       # print(request.session.get_expiry_date())
        return Response({
        "user": CreateUserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1],
        })          
class RegisterUserRestaurant(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_staff=True)
        #print(request.session.get_expiry_date())
        Restaurant.objects.create(user=user,name=user,)
        return Response({
        "user": CreateUserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1],
        })          

##############################################################

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request,format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)



    # Profile end point --> User can be edit his profile and read other profiles
class UserProfileViewSet(generics.RetrieveUpdateAPIView):
   # authentication_classes=(TokenAuthentication ,)
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class= ProfileSerializer
    queryset=Profile.objects.all()
    lookup_field='id' # for url --> /id