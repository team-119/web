from django.db import models

class Patient(models.Model):
    emer = models.IntegerField(default=1) #1:비응, 3:응
    #bed = models.IntegerField(default=0) #0이면 병상 노필요
    oper = models.IntegerField(default=0) #0이면 수술 노필요
    hos = models.CharField(max_length=1, null=True)
    
    ETE_S = models.IntegerField(default=0)
    ETE_C = models.IntegerField(default=0)
    ETE_B = models.IntegerField(default=0)
    ETE_U = models.IntegerField(default=0)
    
    ETA_S = models.IntegerField(default=0)
    ETA_C = models.IntegerField(default=0)
    ETA_B = models.IntegerField(default=0)
    ETA_U = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id)