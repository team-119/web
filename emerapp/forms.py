from django import forms
from emerapp.models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('emer', 'oper',)