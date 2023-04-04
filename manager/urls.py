from django.urls import path
from . import views
from user import views as v



app_name = 'manager'

urlpatterns = [
    path('' , views.ManagerView.as_view() , name='manager') , 
    path('user_accounts/' , v.UserAccountsView.as_view() , name = 'acc')
]