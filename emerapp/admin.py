from django.contrib import admin
from emerapp.models import Patient

class PatientAdmin(admin.ModelAdmin):
    list_display = ['emer', 'oper']

admin.site.register(Patient, PatientAdmin)