from django.shortcuts import render , redirect
# Create your views here.
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin





# class ManagerView(LoginRequiredMixin ,View) : 
#     def dispatch(self, request, *args, **kwargs)  :
#         if request.user.is_authenticated : 
#             if request.user.username != 'hossein' : 
#                 messages.success(request  , 'خطا' , 'warning')
#                 return redirect('user:profile')
#         return super().dispatch(request, *args, **kwargs)

#     def get(self, request ) : 
#         return HttpResponse('hello user')