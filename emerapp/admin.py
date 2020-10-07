from django.contrib import admin
from emerapp.models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('address', 'emergency', 'oper', 'room',)