from django.db import models
#from geoposition.fields import GeopositionField

class Patient(models.Model):
    address = models.CharField(max_length=100, default='')
    emergency = models.IntegerField(default=3)
    oper = models.IntegerField(default=1)
    room = models.IntegerField(default=1)
    #gps = GeopositionField(null=True)
    #t0 = models.IntegerField(default=0)
    #wait_time
    #i
    #tm_1o
    
    def __str__(self):
        return self.address