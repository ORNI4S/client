from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegisterForm(forms.Form) : 
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control' ,
                                                                                   'placeholder' : 'یوزرنیم را وارد کنید'  , 
                                                                                   'class' : 'col-xs-2' , 
                                                                                   'class' : 'text-center'

                                                                                   }) , label='')
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class' : 'form-control' ,
                                                                                   'placeholder' : 'ایمیل را وارد کنید'  , 
                                                                                   'class' : 'col-xs-2' , 
                                                                                   'class' : 'text-center'

                                                                                   }) , label='')
    

    password = forms.CharField(max_length=100  , widget=forms.PasswordInput(attrs={'class' : 'form-control' ,
                                                                                   'placeholder' : 'پسورد را وارد کنید'  , 
                                                                                   'class' : 'col-xs-2' , 
                                                                                   'class' : 'text-center' ,

                                                                                   }) , label='')
    password2 = forms.CharField(max_length=100 , widget=forms.PasswordInput(attrs={'class' : 'form-control' ,
                                                                                   'placeholder' : 'تکرار پسورد را وارد کنید'  , 
                                                                                   'class' : 'col-xs-2' , 
                                                                                   'class' : 'text-center'

                                                                                   }) , label='')




    def clean_username(self ) : 
        username = self.cleaned_data['username']
        check = User.objects.filter(username=username).exists()
        if check : 
            raise ValidationError('این یوزر نیم وجود دارد .')
        return username


    def clean_email(self) : 
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('این ایمیل وجود دارد لطفا ایمیل دیگری استفاده کنید .')
        return email

    def clean(self) : 
        cd = super().clean()
        p1 = cd['password']
        p2 = cd['password2']


        if p1 and p2 and p1 != p2 : 
            raise ValidationError('پسورد ها با هم برابر نیستن .لطفا دوباره تلاش کنید .')
        

class UserLoginForm(forms.Form) : 
    username = forms.CharField(max_length=100  , widget=forms.TextInput(attrs={'class' : 'form-control' ,
                                                                                   'placeholder' : 'یوزرنیم را وارد کنید'  , 
                                                                                   'class' : 'col-xs-2' , 
                                                                                   'class' : 'text-center'

                                                                                   }) , label='')
    password = forms.CharField(max_length=100 , widget=forms.PasswordInput(attrs={'class' : 'form-control' ,
                                                                                   'placeholder' : 'پسورد را وارد کنید'  , 
                                                                                   'class' : 'col-xs-2' , 
                                                                                   'class' : 'text-center'

                                                                                   }) , label='')
    


class get_gift(forms.Form) : 
    code = forms.CharField(max_length=200 , 
                            widget=forms.TextInput(attrs={'class' : 'form-control' ,
                                                                             'placeholder' : 'کد هدیه را وارد کنید ' , 
                                                                             'class' : 'col-xs-2' , 
                                                                             'class' : 'text-center'}) , label='')


class add_fpass(forms.Form) : 
    fpass = forms.CharField(max_length=200  , widget=forms.TextInput(attrs={'class' : 'form-control' ,
                                                                             'placeholder' : 'فروت پس را وارد کنید' , 
                                                                             'class' : 'col-xs-2' , 
                                                                             'class' : 'text-center'}) , label='')
    

    second = forms.IntegerField(widget=forms.TextInput(attrs={'class' : 'form-control' ,
                                                                             'placeholder' : 'ثانیه را وارد کنید' , 
                                                                             'class' : 'col-xs-1' , 
                                                                             'class' : 'text-center' , 
                                                                             'type' : 'number' , 
                                                                             }) , label='')




# username = forms.CharField(widget=forms.TextInput(
#         attrs={
#         'class':'form-control',
#         'placeholder':'Username'
#         }
#     ))