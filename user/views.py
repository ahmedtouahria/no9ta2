import json
from pickle import FALSE
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework import  generics
from resto.models import Meal, MealSubscribe, Restaurant
from user.forms import CreateResto, MealForm, RegisterForm,LoginForm
from user.models import User,Profile
from .serializers import CreateUserSerializer, LoginUserSerializer ,ProfileSerializer
from knox.models import AuthToken
from django.contrib.auth import login , logout
#from rest_framework.authtoken.serializers import AuthTokenSerializer
#from rest_framework.Login import TokenLogin
from .custompermission import IsOwnerOrReadOnly
from knox.views import LoginView as KnoxLoginView
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
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
          # red_code define from url -> api/register/<str:ref_code>
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
##############################################################

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer
    
    def get_post_response_data(self, request, token, instance):
        UserSerializer = self.get_user_serializer_class()
        data = {
            'id':request.user.id,
            'phone':request.user.phone,
           'username':request.user.name,
           'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token
        }
        if UserSerializer is not None:
            data["user"] = UserSerializer(
                request.user,
                context=self.get_context()
            ).data
        return data
    def post(self, request,format=None):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

    # Profile end point --> User can be edit his profile and read other profiles
class UserProfileViewSet(generics.RetrieveUpdateAPIView):
   # Login_classes=(TokenLogin ,)
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class= ProfileSerializer
    queryset=Profile.objects.all()
    lookup_field='id' # for url --> /id
    
def page_not_found(request,exception):
    return render(request,'not-found.html')  


''' Dashboard for restaurant users '''

from django.db.models.functions import TruncDay
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required(login_url='login_resto')
def dashboard(request):
    try:
     resto_user=Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        resto_user=None 
    if request.method == 'POST':
        data_meal = MealForm(request.POST , request.FILES)
        name=request.POST['name']
        price=request.POST['price']
        photos=request.FILES['photos']
        restaurant=resto_user
        if data_meal.is_valid():
           Meal.objects.create(name=name,price=price,photos=photos,restaurant=restaurant)
           return redirect('dashboard')
               
    chart_data = (
            MealSubscribe.objects.filter(resto=resto_user).annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date"))   
    as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
    # complexe query from ORM
    meal_available = (Q(restaurant=resto_user) & Q(isAvailaible=True))
    meal_no_available = (Q(restaurant=resto_user) & Q(isAvailaible=False))
    
    context={
        "resto_user":resto_user,
        "meals":Meal.objects.filter(restaurant=resto_user),
        "count_meal_availlable":Meal.objects.filter(meal_available).count(),
        "count_meal_no_availlable":Meal.objects.filter(meal_no_available).count(),
        
        "count_subscribers" : MealSubscribe.objects.values('user').annotate(user_count=Count('user')).filter(user_count__gt=1).count(),
        "chart_data": as_json,
        "form":MealForm(),
        "resto_name":request.user.name,
        "count":Meal.objects.filter(restaurant=resto_user).count()
    }
    return render(request,'pages/index.html',context)
@login_required(login_url='login_resto')
def users(request):
    try:
     resto_user=Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        resto_user=None 
    context={
        "users_sub":MealSubscribe.objects.filter(resto=resto_user)
    }    
    return render(request,'pages/users.html',context)

def register_resto(request):
    if request.method =='POST':
        formA=RegisterForm(request.POST)
        name=request.POST['name']
        phone=request.POST['phone']
        password=request.POST['password']
        latitude=request.POST['latitude']
        longitude=request.POST['longitude']
        image=request.FILES.get('image')
        #print(image)
        if formA.is_valid():
            if User.objects.filter(name=name).count()<1:
               user=User.objects.create(name=name,phone=phone,country="QA",password=password,is_resto=True)
               Restaurant.objects.create(user=user,name=name,phone=phone,latitude=latitude,longitude=longitude,image=image)
               print("success")
               return redirect("register_resto")
        else:   
         print(" no success")
         messages.error(request,"هذا المطعم موجود , يرجى إسناد إسم أخر للمطعم ")   
        return redirect("dashboard")
         
    context={
        "formA":RegisterForm(),
        "formB":CreateResto(),
     }
    return render(request,'pages/register_resto.html',context)

def login_resto(request):
	if request.method == "POST":
		phone = request.POST["phone"]
		password = request.POST["password"]
		user = authenticate(phone=phone, password=password)
		if user is not None and user.is_resto:
			login(request, user)
			messages.info(request, f"You are now logged in as {user.name}.")
			return redirect("dashboard")
		else:
			messages.error(request,"خطأ في رقم الهاتف او كلمة السر")
	context={
        "form":LoginForm(),
    }
	return render(request,"pages/login_resto.html",context)
@login_required(login_url='login_resto')
def logout_resto(request):
	logout(request)
	messages.info(request, "تم تسجيل الخروج بنجاح") 
	return redirect("login_resto")
@login_required(login_url='login_resto')
def update(request,id):
    
    meal_id=Meal.objects.get(id=id)# var li dernah id rah yethat fih "id" li yji men database
    if request.method == 'POST':
      data_meal = MealForm(request.POST , request.FILES,instance=meal_id)
      if data_meal.is_valid():
            data_meal.save()
            return redirect('dashboard')
            
    else:
      data_meal = MealForm(instance=meal_id)
    contxt={
        'form': data_meal
           }            
    return render(request,"pages/update.html",contxt)
@login_required(login_url='login_resto')
def delete(request,id):
    meal_data = get_object_or_404(Meal,id=id) # rana jebna id mn had method jdida psq sahla
    if request.method == 'POST':
        meal_data.delete()
        return redirect('dashboard')  
      
    return render(request,'pages/delete.html')
@login_required(login_url='login_resto')
def meals(request):
    try:
     resto_user=Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        resto_user=None 
    context={
    "meals":Meal.objects.filter(restaurant=resto_user),

    }
    return render(request,'pages/meals.html',context)