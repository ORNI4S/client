from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate
from . import forms
from django.contrib import messages
from . import models
from manager import models as md
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

class UserRegister(View) : 
    form_class = forms.UserRegisterForm

    def dispatch(self, request, *args, **kwargs)  :
        if request.user.is_authenticated : 
            messages.success(request  , 'ابتدا از حساب خارج شوید سپس دوباره امتحان کنید .' , 'warning')
            return redirect('user:profile')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request) : 

        form = self.form_class
        return render(request , 'user/register.html' , {'form' : form})
         
    def post(self , request) : 
        form = self.form_class(request.POST)
        if form.is_valid() : 
            cd = form.cleaned_data
            User.objects.create_user(cd['username'] , cd['email'] , cd['password'])
            messages.success(request , 'اکانت با موفقیت ایجاد شد . :)' , 'success')
            return redirect('user:profile')
            
        return render(request , 'user/register.html' , {'form' : form})



class UserLogin(View) : 

    form_class = forms.UserLoginForm
    def dispatch(self, request, *args, **kwargs)  :
        if request.user.is_authenticated : 
            messages.success(request  , 'ابتدا از اکانت خارج شوید.سپس وارد شوید .' , 'warning')
            return redirect('user:profile')
        return super().dispatch(request, *args, **kwargs)
    def get(self , request) :
        form = self.form_class 
        return render(request , 'user/login.html' , {'form' : form})
        
    def post(self , request) : 
        form = self.form_class(request.POST)
        if form.is_valid() : 
            cd = form.cleaned_data
            check = authenticate(request , username=cd['username'] , password =cd['password'] )
            if check is not None : 
                login(request , check)
                messages.success(request , 'با موفقیت وارد حساب کاربری شدید .' , 'success')
                return redirect('user:profile')
            messages.success(request  , 'خطا دوباره امتحان کنید .' , 'warning')
            return redirect('user:login')
        



class UserLogOut(LoginRequiredMixin ,View) : 
    def get(self , request) : 
        logout(request)
        messages.success(request  , 'با موفقیت از اکانت خارج شدید.' , 'success')
        return redirect('user:profile')
    

class UserProfile(LoginRequiredMixin , View) : 
    def get(self , request) :
        form = forms.get_gift()
        user = User.objects.get(id = request.user.id)
        days = user.userdata.subscription-datetime.datetime.now().date()
        day = days.days

        if days.days >1 : 
            sub = True
        else :
            sub = False
        return render(request , 'user/profile.html' , {'sub' : sub , 'day' : day , 'form' : form})
    def post(self, request) : 



        form = forms.get_gift(request.POST )
        if form.is_valid() : 
            cd = form.cleaned_data
            check= md.Gift.objects.filter(code = cd['code'])
            if len(check) != 0 : 
                gift= md.Gift.objects.get(code = cd['code'])
                giftuser = models.GiftUser.objects.filter(user = request.user ,gift = gift).exists()
                user = User.objects.get(id = request.user.id)
                if gift.used <= gift.count : 
                    if giftuser == False  : 
                        days = user.userdata.subscription-datetime.datetime.now().date()
                        if days.days < 0 : 
                            new = datetime.datetime.now().date() + datetime.timedelta(days=gift.day)
                            user.userdata.subscription = new
                            user.userdata.account_count += gift.count
                            user.userdata.save()
                            gift.used += 1
                            gift.save()
                            messages.success(request  , 'کد هدیه با موفقیت اعمال شد' , 'success')
                        else:
                            new = user.userdata.subscription + datetime.timedelta(days=gift.day)
                            user.userdata.subscription = new
                            user.userdata.account_count += gift.count
                            user.userdata.save()
                            gift.used += 1
                            gift.save()
                            messages.success(request  , 'کد هدیه با موفقیت اعمال شد' , 'success')
                        models.GiftUser.objects.create(user = request.user , gift = gift)

                    else : 
                        
                        messages.success(request  , 'کد وارد شده تکراری است .' , 'warning')
                else :
                    messages.success(request  , 'کد وارد شده منقضی شده است .' , 'warning')
                    
            else :

                messages.success(request  , 'کد وارد شده اشتباه است .' , 'warning')
                return redirect('user:profile')

# class EditUserView(LoginRequiredMixin, View):
# 	form_class = EditUserForm

# 	def get(self, request):
# 		form = self.form_class(instance=request.user.profile, initial={'email':request.user.email})
# 		return render(request, 'account/edit_profile.html', {'form':form})

# 	def post(self, request):
# 		form = self.form_class(request.POST, instance=request.user.profile)
# 		if form.is_valid():
# 			form.save()
# 			request.user.email = form.cleaned_data['email']
# 			request.user.save()
# 			messages.success(request, 'profile edited successfully', 'success')
# 		return redirect('account:user_profile', request.user.id)



#                     # user.userdata.subscription = datetime.datetime.now().date() + 


                    

                





#             else : 
#                 messages.success(request  , 'کد وارد شده نامعتبر است.' , 'warning')

            # check = authenticate(request , username=cd['username'] , password =cd['password'] )
            # if check is not None : 
            #     login(request , check)
            #     messages.success(request , 'با موفقیت وارد حساب کاربری شدید .' , 'success')
            #     return redirect('user:profile')
            return redirect('user:profile')
        
