from cgitb import handler
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('', include('resto.urls')),
    
    
    
 # path('tokenrequest/', obtain_auth_token)
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404="user.views.page_not_found"