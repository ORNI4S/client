from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from . import models
from user import models as md
import datetime
import requests
import json
from django.db.models.signals import pre_delete
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType



@receiver(post_save  , sender = models.Server )
def add_server(sender  , **kwargs) : 
    if kwargs['created'] : 
        link = kwargs['instance'].link

        id = kwargs['instance'].id
        try : 

            
            if  link[-1] == '/' : 
                server = models.Server.objects.get(id  =id)
                server.link = link[0:-1]
                server.save()


            res = requests.get(link)
            if res.status_code != 200 :

                models.Server.objects.get(id  =id).delete()
            elif res.status_code == 200 :
                if json.loads(res.content)['status'] not in ['off' , 'on'] :
                    models.Server.objects.get(id  =id).delete()


        except : 
            models.Server.objects.get(id  =id).delete()



@receiver(pre_delete, sender=md.UserAccounts)
def mymodel_post_delete(sender, instance, using ,**kwargs):
    content_type = ContentType.objects.get_for_model(md.UserAccounts)
    logs = LogEntry.objects.filter(content_type=content_type, object_id=instance.id)
    if logs.exists():
            res =requests.get(f'{instance.link}/kill/{instance.pid}')
            instance.user.userdata.account_used -= 1
            instance.user.userdata.save()
    else:
        print('#')