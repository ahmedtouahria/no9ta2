import stripe
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView
from djstripe.enums import APIKeyType
from djstripe.models import APIKey
from django.conf import settings
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import Meal, Restaurant, MealSubscribe, SubscribeUser
from .serializers import *
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from datetime import date, timedelta ,datetime
from rest_framework.throttling import UserRateThrottle
from user.models import Profile , User
from rest_framework import status
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# get all meals list to any one 
class MealsList(generics.ListAPIView):
   serializer_class = MealSerializer
   queryset = Meal.objects.all()

# get meal by id
class MealRetrive(generics.RetrieveAPIView):
   serializer_class = MealSerializer
   queryset = Meal.objects.all()
   lookup_field = 'id'
# get resto List to any one
class RestoList(generics.ListAPIView):
   serializer_class = RestoSerializer
   queryset = Restaurant.objects.all()
# get resto by id
class RestoRetrive(generics.RetrieveAPIView):
   serializer_class = RestoSerializer
   queryset = Restaurant.objects.all()
   lookup_field = 'id'
# To ensure that the user cannot exceed 1 subscribe per day
class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'
# To ensure that the user cannot exceed 2 food requests per day
class TowPerDayUserThrottle(UserRateThrottle):
    rate = '2/day'

##########################################################################################
# throttle_classes decorator to implement limitted request per day
@throttle_classes([OncePerDayUserThrottle])
class SubscribePost(generics.CreateAPIView):
   permission_classes = (permissions.IsAuthenticated,)
   serializer_class = SubscriberSerializer
   queryset = SubscribeUser.objects.all()

   # override this function for set current user to user
   @throttle_classes([OncePerDayUserThrottle])
   def perform_create(self, serializer):
      # whene a user subscribes , the recommended user will take profit
        profile = Profile.objects.get(user=self.request.user)
        if profile.recommended_by != None:
         profile_recommended = Profile.objects.get(user=profile.recommended_by)
         profile_recommended.profit += 1.05
         profile_recommended.save()
         print(profile_recommended.profit)
        serializer.save(user=self.request.user)


# throttle_classes decorator to implement limitted request per day

@throttle_classes([TowPerDayUserThrottle])
class SubscribeMealPost(generics.CreateAPIView):
   permission_classes = (permissions.IsAuthenticated,)
   serializer_class = MealSubscribeSerializer
   queryset = MealSubscribe.objects.all()
   # override this function for set current user to user
   def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(user=self.request.user)

 # get list of user foods this week
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def SubscribeMealList(request):
   # for get list of meals last week
   d = date.today()-timedelta(days=7)   
   # print(request.user)
   if request.method == 'GET':
      mealsSubs = MealSubscribe.objects.filter(user=request.user, date__gte=d)
     # print(mealsSubs)
      serializers = MealSubscribeSerializer(mealsSubs, many=True)
      return Response(serializers.data)
   else:
      return Response(f"error method{request.method} not allowed")
   
   ###############################-----# GETWAY PAYMENT WITH STRIPE #----#######################################
##############################------# Used webView #------##################################################
# Get api_key from settings 
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
from django.utils.decorators import method_decorator

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

YOUR_DOMAIN="http://127.0.0.1:8000"
# next step we will create 3 points to payment type [89,130,220] 
#@method_decorator(login_required, name='dispatch')
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
from django.contrib.auth import authenticate, login
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