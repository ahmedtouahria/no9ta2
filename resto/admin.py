import json
from django.contrib import admin
from  .models import Restaurant,Meal,SubscribeUser,MealSubscribe
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.contrib.auth.models import  Group
from knox.models import AuthToken
# Register your models here. 
from djstripe import models


class RestoAdmin(admin.ModelAdmin):
 model=Restaurant   
 list_display = ('name', 'position', 'phone','user')
 def has_add_permission(self, request, obj=None):
        return request.user.is_admin 
 def has_delete_permission(self, request, obj=None):
        return request.user.is_admin
 def has_change_permission(self, request, obj=None):
        return request.user.is_admin or (obj and obj.user == request.user)

#############################################    
class SubscribeAdmin(admin.ModelAdmin):
 model=SubscribeUser   
 list_display = ('user', 'type_sub', 'created_at')
 def has_add_permission(self, request, obj=None):
        return request.user.is_admin
 def has_delete_permission(self, request, obj=None):
        return request.user.is_admin
 def changelist_view(self, request, extra_context=None):
        subscribe_89_count=SubscribeUser.objects.filter(type_sub=89).count()
        subscribe_130_count=SubscribeUser.objects.filter(type_sub=130).count()
        subscribe_220_count=SubscribeUser.objects.filter(type_sub=220).count()
        # Aggregate new subscribers per day
        chart_data = (
            SubscribeUser.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {
       "chart_data": as_json,
       "subscribe_89_count":subscribe_89_count,
       "subscribe_130_count":subscribe_130_count,
       "subscribe_220_count":subscribe_220_count,
       
       }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
###############################################
class MealAdmin(admin.ModelAdmin):
 model=Meal   
 list_display = ('name', 'price', 'restaurant')
 def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Meal.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context) 
 ########################################
class MealSubAdmin(admin.ModelAdmin):
 model=MealSubscribe   
 list_display = ('user', 'food', 'code','resto','created_at')
 readonly_fields=('code',)
 search_fields=('user','food')
 def has_add_permission(self, request, obj=None):
        return request.user.is_admin
 def has_delete_permission(self, request, obj=None):
        return request.user.is_admin   

 
 def changelist_view(self, request, extra_context=None):
        resto_of_staff=Restaurant.objects.get(user=request.user)
        print(resto_of_staff)
        food_resto = MealSubscribe.objects.filter(resto=resto_of_staff)
        print(food_resto)
        # Aggregate new subscribers per day
        if request.user.is_admin:
         chart_data = (
            MealSubscribe.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date"))
        else:
            chart_data = (
            MealSubscribe.objects.filter(resto=resto_of_staff).annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date"))
            
        # get most meal subscribe
        # 
        more = MealSubscribe.objects.values_list('food').annotate(sub_count=Count('food')).order_by('-sub_count')
        #print(more[0][0])
       # most_food_ID=more[0][0]
        #most_food = Meal.objects.get(id=most_food_ID)
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {
               "chart_data": as_json,
              # "most_food":most_food
               }

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
 
 
admin.site.register(Restaurant,RestoAdmin)
admin.site.register(Meal,MealAdmin)
admin.site.register(SubscribeUser,SubscribeAdmin)
admin.site.register(MealSubscribe,MealSubAdmin)
admin.site.unregister(Group)
#admin.site.unregister(models.APIKey)
admin.site.unregister(models.Account)
admin.site.unregister(models.ApplicationFeeRefund)
admin.site.unregister(models.ApplicationFee)
admin.site.unregister(models.BankAccount)
admin.site.unregister(models.BalanceTransaction)
admin.site.unregister(models.Charge)
admin.site.unregister(models.Customer)
admin.site.unregister(models.Coupon)
admin.site.unregister(models.Card)
admin.site.unregister(models.Dispute)
admin.site.unregister(models.Event)
#admin.site.unregister(models.FileLink)
admin.site.unregister(models.File)
admin.site.unregister(models.IdempotencyKey)
admin.site.unregister(models.Invoice)
admin.site.unregister(models.Mandate)
admin.site.unregister(models.PaymentIntent)
admin.site.unregister(models.PaymentMethod)
admin.site.unregister(models.Payout)
admin.site.unregister(models.Plan)
admin.site.unregister(models.Price)
admin.site.unregister(models.Product)
admin.site.unregister(models.Refund)
admin.site.unregister(models.Session)
admin.site.unregister(models.SetupIntent)
admin.site.unregister(models.Source)
admin.site.unregister(models.Subscription)
admin.site.unregister(models.TaxRate)
admin.site.unregister(models.TransferReversal)
admin.site.unregister(models.Transfer)
admin.site.unregister(models.UsageRecordSummary)
admin.site.unregister(models.UsageRecord)
admin.site.unregister(models.WebhookEventTrigger)






