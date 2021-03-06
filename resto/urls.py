from django.urls import path, include
from .views import *
from rest_framework import routers
router = routers.DefaultRouter()
router.register('resto', RestaurantViewSetList)
router.register('meals', MealViewSet)

urlpatterns = [
    path('mealsubscribe/', SubscribeMealPost.as_view()),
    path("mealsubscribe/list/", SubscribeMealList),
    path('', include(router.urls)),
    path('test_payment/',test_payment),
    path('save_stripe_info/',save_stripe_info),


    #--------------PAYMENT GATWAY------------------#
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path(
        "checkout/redirect89/<str:session_id>",
        checkout_redirect89,
        name="checkout_redirect89",
    ),
    path(
        "checkout/redirect130/<str:session_id>",
        checkout_redirect130,
        name="checkout_redirect130",
    ),
    path(
        "checkout/redirect220/<str:session_id>",
        checkout_redirect220,
        name="checkout_redirect220",
    ),
    path("stripe/thankyou/89", thankyou_89, name="thankyou89"),
    path("stripe/thankyou/130", thankyou_130, name="thankyou130"),
    path("stripe/thankyou/220", thankyou_220, name="thankyou220"),

    path("checkout/create/89", create_checkout_session_89,
         name="create_checkout_session_89"),
    path("checkout/create/130", create_checkout_session_130,
         name="create_checkout_session_130"),
    path("checkout/create/220", create_checkout_session_220,
         name="create_checkout_session_220"),
    # path('stripe/subscription',subscriptionStripeView,name='subscribtions'),
    path('stripe/login/89', loginPageStripe89, name='login89'),
    path('stripe/login/130', loginPageStripe130, name='login130'),
    path('stripe/login/220', loginPageStripe220, name='login220'),


]
