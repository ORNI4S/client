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



class UserAccounts(models.Model) : 
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='accounts')
    fpass = models.CharField(max_length=200 , default=None)
    link = models.CharField(max_length=250 , null=True  ,blank=True)
    second = models.PositiveIntegerField(default=180)
    pid = models.IntegerField(default=0)
    collected_gold = models.CharField(max_length=200 , default=None)
    player_gold = models.CharField(max_length=200 , default=None)
    gold_collection_allowed = models.CharField(max_length=200 , default=None)
    gold_collection_allowed_at = models.CharField(max_length=200 , default=None)
    gold_collection_extraction = models.CharField(max_length=200 , default=None)
    last_gold_collect_at = models.CharField(max_length=200 , default=None)
    needs_captcha = models.CharField(max_length=200 , default=None)
