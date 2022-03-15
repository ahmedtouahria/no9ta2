from .views import *
from django.urls import path,include
from rest_framework import routers
from knox import views as knox_views

#router = routers.DefaultRouter()
#router.register('api',UserProfileViewSet)

urlpatterns = [
path('api/register/', RegisterUserWithOutSession.as_view(), name='register'),
path('api/register/<str:ref_code>', RegisterUserAPIView.as_view(), name='register'),

path('api/login/', LoginAPI.as_view(), name='login'),
path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
#path('profile/',include(router.urls)),
path("profile/<int:id>/", UserProfileViewSet.as_view(), name="profile"),
path("resto/dashboard", dashboard, name="dashboard"),
path("resto/dashboard/users", users, name="users"),
path("resto/register", register_resto, name="register_resto"),
path("resto/login", login_resto, name="login_resto"),
path("resto/logout", logout_resto, name="logout_resto"),
path("resto/meals", meals, name="meals"),
path('resto/update/<int:id>',update,name='update'),
path('resto/delete/<int:id>',delete,name='delete'),


]