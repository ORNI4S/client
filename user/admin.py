from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from . import models





class UserDataInline(admin.StackedInline) : 
    model = models.UserData

class ExtendedUserAdmin(UserAdmin) : 
    inlines = (UserDataInline , )

admin.site.register(models.UserAccounts)

admin.site.register(models.GiftUser)


admin.site.unregister(User)
admin.site.register(User , ExtendedUserAdmin)