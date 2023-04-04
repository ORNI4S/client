from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from . import models
import datetime
import requests
import json





@receiver(post_save  , sender = models.Server )
def add_server(sender  , **kwargs) : 
    if kwargs['created'] : 
        link = kwargs['instance'].link
        id = kwargs['instance'].id
        try : 


            res = requests.get(link)
            if res.status_code != 200 :

                models.Server.objects.get(id  =id).delete()
            elif res.status_code == 200 :
                if json.loads(res.content)['status'] not in ['off' , 'on'] :
                    models.Server.objects.get(id  =id).delete()
                
                    



                    



        except : 
            models.Server.objects.get(id  =id).delete()


# 

        # res = requests.get(link)
        # if res.status_code != 200 : 
        #     models.Server.objects.get(id  =id).delete()
        # day = requests.get()
        # models.UserData.objects.create(user = kwargs['instance'], subscription = day)
        print('*' * 100)