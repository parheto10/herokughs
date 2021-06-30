from django import forms
from django.contrib.auth.models import User
from django.forms import DateInput, CheckboxSelectMultiple

from parametres.models import Symptome
from patients.models import Patient, Rdv
from .models import Personnel

class DocteurForm(forms.ModelForm):
    class Meta:
        model= Personnel
        fields=[
            'matricule',
            'genre',
            'grade',
            'hopital',
            'service',
            'telephone1',
            'telephone2',
            'adresse',
            'bio',
            'avatar',
        ]

class EditRdvAdminForm(forms.ModelForm):
    patient=forms.ModelChoiceField(queryset=Patient.objects.all(),empty_label="Patient")
    symptomes = forms.ModelMultipleChoiceField(queryset=Symptome.objects.all(), widget=CheckboxSelectMultiple)
    date_rdv = DateInput()
    class Meta:
        model=Rdv
        widgets = {
            'date_rdv': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%YT%H:%M'),
        }
        fields=[
            'code',
            'date_rdv',
            'patient',
            'poids',
            'taille',
            'diastolique',
            'systolique',
            'ta',
            'symptomes',
            'alert',
            'last_examen',
            'details'
        ]
    def __init__(self, *args, **kwargs):
        super(EditRdvAdminForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['date_rdv'].input_formats = ('%d/%m/%YT%H:%M',)

    def Tension(self):
        if self.diastolique and self.systolique:
            self.ta = (self.diastolique + self.systolique) / 2