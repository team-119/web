from django.contrib import admin
from emerapp.models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'emer', 'oper', 'hos', 'by', 'start', 'end', 'ETE_S', 'ETE_C', 'ETE_B', 'ETE_U', 'ETA_S', 'ETA_C', 'ETA_B', 'ETA_U']

admin.site.register(Patient, PatientAdmin)