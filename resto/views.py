import stripe
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from djstripe.enums import APIKeyType
from djstripe.models import APIKey
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, permissions,viewsets,status
from .models import Meal, Restaurant, MealSubscribe, SubscribeUser
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, throttle_classes,action
from datetime import date, timedelta
from rest_framework.throttling import UserRateThrottle
from user.models import Profile , User
#from rest_framework import status
from django.shortcuts import render, redirect 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# get all meals list to any one 
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to delete '
            }    
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=['post'])
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            '''
            create or update 
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            print(int(stars)==4)
            # username = request.data['username']
            # user = User.objects.get(username=username)                
            try:
                # update
               if int(stars) > 0 and int(stars) <6:
                rating = Rating.objects.get(user=user.id, meal=meal.id) # specific rate 
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Updated',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_200_OK)
               else:
                   return Response({"rate stars must be between [1,5]"} , status=status.HTTP_400_BAD_REQUEST)

            except:
                # create if the rate not exist 
               if int(stars) > 0 and int(stars) <6:
                    
                rating = Rating.objects.create(stars=stars, meal=meal, user=user)
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Created',
                    'result': serializer.data
                }
                return Response(json , status=status.HTTP_200_OK)
               else:
                   return Response({"rate stars must be between [1,5]"} , status=status.HTTP_400_BAD_REQUEST)

        else:
            json = {
                'message': 'stars not provided'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)


# To ensure that the user cannot exceed 1 subscribe per day
class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'
# To ensure that the user cannot exceed 2 food requests per day
class TowPerDayUserThrottle(UserRateThrottle):
    rate = '2/day'


# throttle_classes decorator to implement limitted request per day

@throttle_classes([TowPerDayUserThrottle])
class SubscribeMealPost(generics.CreateAPIView):
   permission_classes = (permissions.IsAuthenticated,)
   serializer_class = MealSubscribeSerializer
   queryset = MealSubscribe.objects.all()
   # override this function for set current user to user
   def perform_create(self, serializer):
       # print(self.request.user)
       # business code for ensure to user is subscribed in last week ;)
        d = date.today()-timedelta(days=7)
        userSub = SubscribeUser.objects.filter(user=self.request.user, created_at__gte=d).count()
        if userSub>0:
         serializer.save(user=self.request.user)
        else:
            pass 
 # get list of user foods this week
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def SubscribeMealList(request):
   # for get list of meals last week
   d = date.today()-timedelta(days=7)   
   # print(request.user)
   if request.method == 'GET':
      mealsSubs = MealSubscribe.objects.filter(user=request.user, created_at__gte=d)
     # print(mealsSubs)
      serializers = MealSubscribeSerializer(mealsSubs, many=True)
      return Response(serializers.data)
   else:
      return Response(f"error method{request.method} not allowed")

# get resto and meal to specified resto 
class RestaurantViewSetList(viewsets.ModelViewSet):
    queryset = Restaurant.objects.filter(active=True)
    serializer_class = RestoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    @action(detail=True)
    def getMealsList(self, request, pk=None):
        resto=Restaurant.objects.get(id=pk)
        meals_list=Meal.objects.filter(restaurant=resto)
        serializer = MealSerializer(meals_list, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }

        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    def create(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to create or update '
            }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        response = {
            'message': 'Invalid way to delete '
            }    
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
   ###############################-----# GETWAY PAYMENT WITH STRIPE #----#######################################
##############################------# Used webView #------##################################################
# Get api_key from settings 
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
#checkout stripe webview 
#@method_decorator(login_required, name='dispatch')

class CheckoutRedirectView89(LoginRequiredMixin,TemplateView,):
    login_url = 'login89'
    template_name = "checkout_redirect.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        public_keys = APIKey.objects.filter(type=APIKeyType.publishable)[:1]
        if not public_keys.exists():
            url = self.request.build_absolute_uri(
                "/admin/djstripe/apikey/add/")
            raise ImproperlyConfigured(
                "You must first configure a public key. "
                + f"Go to {url} to input your public key."
            )
        # override context to read "stripe_public_key" from html / js files
        ctx["stripe_public_key"] = public_keys.get().secret
        ctx["checkout_session_id"] = self.kwargs["session_id"]

        return ctx
class CheckoutRedirectView130(LoginRequiredMixin,TemplateView,):
    login_url = 'stripe/login/130'
    template_name = "checkout_redirect.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        public_keys = APIKey.objects.filter(type=APIKeyType.publishable)[:1]
        if not public_keys.exists():
            url = self.request.build_absolute_uri(
                "/admin/djstripe/apikey/add/")
            raise ImproperlyConfigured(
                "You must first configure a public key. "
                + f"Go to {url} to input your public key."
            )
        # override context to read "stripe_public_key" from html / js files
        ctx["stripe_public_key"] = public_keys.get().secret
        ctx["checkout_session_id"] = self.kwargs["session_id"]

        return ctx
class CheckoutRedirectView220(LoginRequiredMixin,TemplateView,):
    login_url = 'login220'
    template_name = "checkout_redirect.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        public_keys = APIKey.objects.filter(type=APIKeyType.publishable)[:1]
        if not public_keys.exists():
            url = self.request.build_absolute_uri(
                "/admin/djstripe/apikey/add/")
            raise ImproperlyConfigured(
                "You must first configure a public key. "
                + f"Go to {url} to input your public key."
            )
        # override context to read "stripe_public_key" from html / js files
        ctx["stripe_public_key"] = public_keys.get().secret
        ctx["checkout_session_id"] = self.kwargs["session_id"]

        return ctx




checkout_redirect89 = CheckoutRedirectView89.as_view()
checkout_redirect130 = CheckoutRedirectView130.as_view()
checkout_redirect220 = CheckoutRedirectView220.as_view()

#YOUR_DOMAIN="http://127.0.0.1:8000"
YOUR_DOMAIN="https://noqtaa.herokuapp.com"
# next step we will create 3 points to payment type [89,130,220] 
class CreateCheckoutSession_89(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
       # print(self.request.user.phone)
        #get price id from settings conf and stripe dashboard
        price=settings.STRIPE_PRICE_TYPE_89
        #print(self.request.user)
        checkout_session=stripe.checkout.Session.create(
            client_reference_id=self.request.user,
            success_url=YOUR_DOMAIN+"/stripe/thankyou/89?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=YOUR_DOMAIN+"/checkout/canceled/",
            mode="subscription",
            line_items=[{"price": price, "quantity": 1}],
            payment_method_types=["card"],
        )
        print(checkout_session)
        return reverse(
            "checkout_redirect89", kwargs={"session_id": checkout_session["id"]}
        )
class CreateCheckoutSession_220(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        print("name"+str(self.request.user.id))
        #print(self.request.user)
        price=settings.STRIPE_PRICE_TYPE_220
        checkout_session=stripe.checkout.Session.create(
            client_reference_id=self.request.user,
            success_url=YOUR_DOMAIN+"/stripe/thankyou/220?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=YOUR_DOMAIN+"/checkout/canceled/",
            mode="subscription",
            line_items=[{"price": price, "quantity": 1}],
            payment_method_types=["card"],
        )

        print(checkout_session)

        return reverse(
            "checkout_redirect220", kwargs={"session_id": checkout_session["id"]}
        )
class CreateCheckoutSession_130(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        price=settings.STRIPE_PRICE_TYPE_130
        checkout_session=stripe.checkout.Session.create(
            client_reference_id=self.request.user,
            success_url=YOUR_DOMAIN+"/stripe/thankyou/130?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=YOUR_DOMAIN+"/checkout/canceled/",
            mode="subscription",
            line_items=[{"price": price, "quantity": 1}],
            payment_method_types=[],
        )
        print(checkout_session)
        return reverse(
            "checkout_redirect130", kwargs={"session_id": checkout_session["id"]}
        )
def thankyou_89(request):
   #print(request.user.phone)
   try:
    subscribe_user = SubscribeUser.objects.filter(user=request.user).first()
    if subscribe_user != None:
     d = date.today()-timedelta(days=7)
     userSub = SubscribeUser.objects.filter(user=request.user, created_at__gte=d) 
     if userSub.count()>=1:
         pass
     else:
       SubscribeUser.objects.create(user=request.user,type_sub=89) 
    else:
       SubscribeUser.objects.create(user=request.user,type_sub=89) 
   except SubscribeUser.DoesNotExist:
       pass    
   context={
      'user_name':request.user.name,
      'STRIPE_PUBLIC_KEY': APIKey.objects.filter(type=APIKeyType.publishable)[:1].get().secret
   }
   return render(request, 'success_url.html', context)
def thankyou_130(request):
   try:
    subscribe_user = SubscribeUser.objects.filter(user=request.user).first()
    if subscribe_user != None:
     d = date.today()-timedelta(days=7)
     userSub = SubscribeUser.objects.filter(user=request.user, created_at__gte=d) 
     if userSub.count()>=1:
         pass
     else:
       SubscribeUser.objects.create(user=request.user,type_sub=130) 
    else:
       SubscribeUser.objects.create(user=request.user,type_sub=130) 
   except SubscribeUser.DoesNotExist:
       pass 
   context={
       'user_name':request.session.get('phone',default='def'),
      'STRIPE_PUBLIC_KEY': APIKey.objects.filter(type=APIKeyType.publishable)[:1].get().secret
   }
   return render(request, 'success_url.html', context)
def thankyou_220(request):
   try:
    subscribe_user = SubscribeUser.objects.filter(user=request.user).first()
    if subscribe_user != None:
     d = date.today()-timedelta(days=7)
     userSub = SubscribeUser.objects.filter(user=request.user, created_at__gte=d) 
     if userSub.count()>=1:
         pass
     else:
       SubscribeUser.objects.create(user=request.user,type_sub=220) 
    else:
       SubscribeUser.objects.create(user=request.user,type_sub=220) 
   except SubscribeUser.DoesNotExist:
       pass 
   context={
       'user_name':request.user.name,
      'STRIPE_PUBLIC_KEY': APIKey.objects.filter(type=APIKeyType.publishable)[:1].get().secret
   }
   return render(request, 'success_url.html', context)
# function to authenticated user to subscribe and payment
from django.contrib.auth import  login
from django.contrib import messages
def loginPageStripe89(request):
    if request.user.is_authenticated:
        return redirect('create_checkout_session_89')
    else:
      if request.method=='POST':
        phone = request.POST.get('phone')
#        password=request.POST.get('password')
        if User.objects.filter(phone=phone).exists(): 
           user = User.objects.get(phone=phone)
        else:
            user=None
               
        #print(user)
        try:
         if user is not None:
            login(request,user)
            return redirect('create_checkout_session_89')
         else:
            messages.info(request, 'phone is incorrect')
        except User.DoesNotExist:
           return redirect('login89')
                
    context={}        		
    return render(request,'login.html',context)
def loginPageStripe130(request):
    if request.user.is_authenticated:
        return redirect('create_checkout_session_130')
    else:
      if request.method=='POST':
        phone = request.POST.get('phone')
#        password=request.POST.get('password')
        if User.objects.filter(phone=phone).exists(): 
           user = User.objects.get(phone=phone)
        else:
            user=None
               
        #print(user)
        try:
         if user is not None:
            login(request,user)
            return redirect('create_checkout_session_130')
         else:
            messages.info(request, 'phone is incorrect')
        except User.DoesNotExist:
           return redirect('login130')
    context={}        		
    return render(request,'login.html',context)
def loginPageStripe220(request):
    if request.user.is_authenticated:
        return redirect('create_checkout_session_220')
    else:
      if request.method=='POST':
        phone = request.POST.get('phone')
#        password=request.POST.get('password')
        if User.objects.filter(phone=phone).exists(): 
           user = User.objects.get(phone=phone)
        else:
            user=None
               
        #print(user)
        try:
         if user is not None:
            login(request,user)
            return redirect('create_checkout_session_220')
         else:
            messages.info(request, 'phone is incorrect')
        except User.DoesNotExist:
           return redirect('login220')
    context={}        		
    return render(request,'login.html',context)

# function to run subscriptions list to user
 
""" @login_required(login_url='login')
def subscriptionStripeView(request):
    return render(request,'subscriptions.html') """

# end points 

""" class getUserDataForStripe(generics.GenericAPIView):
    def post(self,request ,*args, **kwargs):
        if request.method == 'POST':
           phone = request.POST['phone']
           type_sub = request.POST['type_sub']
           request.session['phone'] = phone
           request.session['type_sub'] = type_sub
        return Response({"phone":phone,"type_sub":type_sub})   """
create_checkout_session_89=CreateCheckoutSession_89.as_view()
create_checkout_session_130=CreateCheckoutSession_130.as_view()
create_checkout_session_220=CreateCheckoutSession_220.as_view()
