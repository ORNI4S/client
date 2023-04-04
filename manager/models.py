from django.db import models

# Create your models here.
class Gift(models.Model) : 
    code = models.CharField(max_length=100)
    day = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    used = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.code} - count {self.count} - used {self.used} - day {self.day}'



# class Server(models.Model) : 
#     link = models.CharField(max_length=200)
#     status = models.BooleanField()