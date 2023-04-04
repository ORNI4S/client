from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from manager import models as md




class UserData(models.Model) : 
    user = models.OneToOneField(User,on_delete=models.CASCADE , related_name='userdata' )
    subscription = models.DateField()
    account_count = models.IntegerField(default=0)
    account_used = models.IntegerField(default=0 , null=True , blank=True)


class GiftUser(models.Model) : 
    gift = models.ForeignKey(md.Gift , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete=models.CASCADE)