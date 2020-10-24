from django.db import models

class Patient(models.Model):
    emer = models.IntegerField(default=1) #1:비응, 3:응
    oper = models.IntegerField(default=0) #0이면 수술 노필요
    hos = models.CharField(max_length=1, null=True)
    by = models.IntegerField(default=0) #0이면 구급대원, 1이면 병
    
    ETE_S = models.CharField(default=0, max_length=5)
    ETE_C = models.CharField(default=0, max_length=5)
    ETE_B = models.CharField(default=0, max_length=5)
    ETE_U = models.CharField(default=0, max_length=5)
    
    ETA_S = models.CharField(default=0, max_length=5)
    ETA_C = models.CharField(default=0, max_length=5)
    ETA_B = models.CharField(default=0, max_length=5)
    ETA_U = models.CharField(default=0, max_length=5)
    
    def __str__(self):
        return str(self.id)