from django import forms
from emerapp.models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('emer', 'oper', 'hos', 'by', 'time', 'ETE_S', 'ETE_C', 'ETE_B', 'ETE_U', 'ETA_S', 'ETA_C', 'ETA_B', 'ETA_U',)