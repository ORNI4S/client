from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login , logout , authenticate
from . import forms
from django.contrib import messages
from . import models
import requests
from manager import models as md
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import json





class UserRegister(View) : 
    form_class = forms.UserRegisterForm

    def dispatch(self, request, *args, **kwargs)  :
        if request.user.is_authenticated : 
            messages.success(request  , 'ابتدا از حساب خارج شوید سپس دوباره امتحان کنید .' , 'warning')
            return redirect('user:login')
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
    def dispatch(self, request, *args, **kwargs)  :
            if request.user.is_superuser: 
                messages.success(request  , 'پنل مدیریت ادمین خوش اومدی :)' , 'success')
                return redirect('manager:manager')
            return super().dispatch(request, *args, **kwargs)
    


    def get(self , request) :
        
        form = forms.get_gift()
        account_form = forms.add_fpass()
        user = User.objects.get(id = request.user.id)
        days = user.userdata.subscription-datetime.datetime.now().date()
        day = days.days

        if days.days >1 : 
            sub = True
        else :
            sub = False
            user.userdata.account_count = 0
            user.userdata.account_used = 0
            user.userdata.save()
            
        useracc = models.UserAccounts.objects.filter(user = request.user.id)
        if useracc.exists() : 
            for i in useracc : 
                NameOP= {'User-Agent' : "Dalvik/2.1.0 (Linux; U; Android 13; SM-A326B Build/TP1A.220624.014)" ,'Connection':'close','Content-Type':"application/x-www-form-urlencoded" ,'Cookie':"FRUITPASSPORT="f"{i.fpass}"}
                data = requests.get('http://iran.fruitcraft.ir/cards/collectgold' , headers = NameOP)
                content = data.content
                if data.status_code == 200 and  len(content) < 500: 
                    x = json.loads(data.content)
                    redata = x['data']
                    acc = models.UserAccounts.objects.get(id = i.id)
                    acc.collected_gold = str(redata.get('collected_gold')) , 
                    acc.player_gold = str(redata.get('player_gold')) , 
                    acc.gold_collection_allowed = str(redata.get('gold_collection_allowed')), 
                    acc.gold_collection_allowed_at = str(redata.get('gold_collection_allowed_at')) , 
                    acc.gold_collection_extraction = str(redata.get('gold_collection_extraction')) , 
                    acc.last_gold_collect_at = str(redata.get('last_gold_collect_at')) , 
                    acc.needs_captcha = str(redata.get('needs_captcha')) , 
                    acc.save()
        acc = models.UserAccounts.objects.filter(user = request.user.id)
            

        return render(request , 'user/profile.html' , {'sub' : sub , 'day' : day , 'form' : form , 'account_form' : account_form , 'useracc' :acc})
    


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
            return redirect('user:profile')
        messages.success(request  , 'کد وارد شده اشتباه است .' , 'warning')
        return redirect('user:profile')
        
        



class UserAccountsView(LoginRequiredMixin , View) : 
    def post(self, request) : 
        form = forms.add_fpass(request.POST)
        if form.is_valid() : 
            cd = form.cleaned_data
            if cd['fpass'].isascii():
                
                NameOP= {'User-Agent' : "Dalvik/2.1.0 (Linux; U; Android 13; SM-A326B Build/TP1A.220624.014)" ,'Connection':'close','Content-Type':"application/x-www-form-urlencoded" ,'Cookie':"FRUITPASSPORT="f"{cd['fpass']}"}
                data = requests.get('http://iran.fruitcraft.ir/cards/collectgold' , headers = NameOP)
                content = data.content
                print(content)
                if len(content) < 500 : 
                    x = json.loads(data.content)
                    redata = x['data']
                    check = models.UserAccounts.objects.filter(fpass = cd['fpass']).exists()
                    if check == False : 
                            if request.user.userdata.account_used < request.user.userdata.account_count :
                                servers =  md.Server.objects.all()
                                if len(servers) > 0 :
                                    for i in servers : 
                                        res = requests.get(i.link)
                                        if res.status_code  == 200 :
                                            w1  ,w2 = json.loads(res.content)['worker1']['status'] , json.loads(res.content)['worker2']['status']
                                            if w1 == 'off' or w2 == 'off' : 

                                                fpass = cd['fpass']
                                                userid = request.user.id
                                                day = request.user.userdata.subscription-datetime.datetime.now().date()
                                                send = requests.get(f'{i.link}/sender/{fpass}/{day.days}/{userid}/200')
                                                
                                                if send.status_code == 200 : 
                                                    jsend = json.loads(send.content)
                                                    if jsend['status'] != 'duplicate' : 
                                                        models.UserAccounts.objects.create(user = request.user ,
                                                                                        link= i.link , 
                                                                                        fpass = cd['fpass'] , 
                                                                                        pid = jsend['pid'] ,
                                                                                        collected_gold = redata['collected_gold'] , 
                                                                                        player_gold = redata['player_gold'] , 
                                                                                        gold_collection_allowed = redata['gold_collection_allowed'], 
                                                                                        gold_collection_allowed_at = redata['gold_collection_allowed_at'] , 
                                                                                        gold_collection_extraction = redata['gold_collection_extraction'] , 
                                                                                        last_gold_collect_at = redata['last_gold_collect_at'] , 
                                                                                        needs_captcha = redata['needs_captcha'])
                                                        request.user.userdata.account_used += 1
                                                        request.user.userdata.save()
                                                        
                                                
                                                        
                                                        messages.success(request  , 'اکانت شما با موفقیت افزوده شد .' , 'success')
                                                        return redirect('user:profile')
                                                        break
                                                          
                                                    else : 
                                                        messages.success(request  , 'پاسخی از سرور دریافت نشد .' , 'success')
                                                        return redirect('user:profile')
                                                else : 
                                                    messages.success(request  , 'پاسخی از سرور دریافت نشد .' , 'success')
                                                    return redirect('user:profile')
                                        else : 
                                            messages.success(request  , 'پاسخی از سرور دریافت نشد .' , 'success')
                                            return redirect('user:profile')

                                else :
                                    messages.success(request  , 'ظرفیت سرور ها تکمیل .لطفا بعدا امتحان کنید .' , 'warning')
                                    return redirect('user:profile')

                            else : 
                                messages.success(request  , 'سقف مجاز اکانت' , 'success')
                                return redirect('user:profile')

                    
                    else : 
                        messages.success(request  , 'اکانت شما با موفقیت افزوده شد .' , 'success')
                        return redirect('user:profile')

                else : 
                    messages.success(request  , 'خطا : یا فروت پس اشتباهه یا سرور در دسترس نیست .' , 'warning')
                    return redirect('user:profile')
            else :
                messages.success(request  ,'خطا :فروت پس اشتباهه' , 'warning')
                return redirect('user:profile')

        return redirect('user:profile')



class KillFpass(LoginRequiredMixin , View) : 
    def get(self , request , fpass) : 
        get_fpass = models.UserAccounts.objects.filter(fpass = fpass)
        if get_fpass.exists() : 
            fp = models.UserAccounts.objects.get(fpass = fpass)
            res =requests.get(f'{fp.link}/kill/{fp.pid}')
            if res.status_code == 200 : 
                get_fpass.delete()
                request.user.userdata.account_used -= 1
                request.user.userdata.save()
                messages.success(request  , 'اکانت شما با موفقیت حذف شد .' , 'success')
                return redirect('user:profile')
            else : 
                messages.success(request  , 'پاسخی از سرور دریافت نشد .' , 'warning')
                return redirect('user:profile')
        messages.success(request  , 'یافت نشد' , 'warning')
        return redirect('user:profile')
        




#667d340953f5bd85db91f06e2d9c4150