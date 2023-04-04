from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from . import models
import datetime




@receiver(post_save  , sender = User )
def add_data(sender  , **kwargs) : 
    if kwargs['created'] : 
        day = datetime.datetime.now() - datetime.timedelta(1)
        models.UserData.objects.create(user = kwargs['instance'], subscription = day)
        print('*' * 100)