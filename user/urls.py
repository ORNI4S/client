from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [
    path('register/' , views.UserRegister.as_view() , name='register') , 
    path('login/' , views.UserLogin.as_view() , name='login') , 
    path('logout/' , views.UserLogOut.as_view() , name = 'logout') , 
    path('' , views.UserProfile.as_view() , name='profile') , 
    path('kill/<str:fpass>' , views.KillFpass.as_view() , name='kill')
]