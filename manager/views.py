from django.shortcuts import render , redirect
# Create your views here.
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
import requests




ADMIN_USER = 'alireza'

class ManagerView(LoginRequiredMixin ,View) : 
    def dispatch(self, request, *args, **kwargs)  :
        if request.user.is_authenticated : 
            if request.user.username != ADMIN_USER : 
                messages.success(request  , 'شما کاربر ادمین نیستی :(' , 'warning')
                return redirect('user:profile')
        return super().dispatch(request, *args, **kwargs)
    




    def get(self, request ) : 
        active = []
        servers = models.Server.objects.all()
        for i in servers : 
            try :
                res= requests.get(i.link)
                if res.status_code == 200 :
                    active.append(i) 
                else : 
                    models.Server.objects.get(id = i.id ).delete()
            except : 
                    models.Server.objects.get(id = i.id ).delete()



        return render(request , 'manager/admin.html' , {'servers' : active})
    