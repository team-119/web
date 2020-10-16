from django.db import models

class Patient(models.Model):
    emer = models.IntegerField(default=1) #1:비응, 3:응
    oper = models.IntegerField(default=0) #0이면 수술 노필요
    
    def __str__(self):
        return str(self.emer) #id를 기준으로 리턴
    
class bed(models.Model):
    sm = models.TextField(blank=True)
    choo = models.TextField(blank=True)
    back = models.TextField(blank=True)
    nmc = models.TextField(blank=True)