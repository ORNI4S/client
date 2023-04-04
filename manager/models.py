from django.db import models
from django.contrib.auth.models import User




# Create your models here.
class Gift(models.Model) : 
    code = models.CharField(max_length=100)
    day = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    used = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.code} - count {self.count} - used {self.used} - day {self.day}'



class Server(models.Model) : 
    link = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.link
    

class RunModel(models.Model) : 
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    server = models.ForeignKey(Server , on_delete=models.CASCADE)
    account = models.CharField(max_length=200)
    second = models.IntegerField()
    pid = models.IntegerField(default=0)
    second = models.IntegerField(default=0)


