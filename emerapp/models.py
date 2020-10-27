from django.db import models

class Patient(models.Model):
    emer = models.IntegerField(default=1) #1:비응, 3:응
    oper = models.IntegerField(default=0) #0이면 수술 노필요
    hos = models.CharField(default="-", max_length=1) #0:성모, 1:의료원, 2:백, 3:추
    by = models.IntegerField(default=0) #0:user_input, 1:hos_input
    time = models.CharField(default="0", max_length=45) #현재시간 
    
    ETE_S = models.CharField(default="0", max_length=5, blank=True)
    ETE_C = models.CharField(default="0", max_length=5, blank=True)
    ETE_B = models.CharField(default="0", max_length=5, blank=True)
    ETE_U = models.CharField(default="0", max_length=5, blank=True)
    
    ETA_S = models.CharField(default="0", max_length=5, blank=True)
    ETA_C = models.CharField(default="0", max_length=5, blank=True)
    ETA_B = models.CharField(default="0", max_length=5, blank=True)
    ETA_U = models.CharField(default="0", max_length=5, blank=True)
    
    start = models.CharField(default="0", max_length=10, blank=True)
    end = models.CharField(default="0", max_length=10, blank=True)
    
    def __str__(self):
        return str(self.id)