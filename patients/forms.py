from django.forms import forms, ModelForm, DateInput, ModelChoiceField, ModelMultipleChoiceField, CheckboxSelectMultiple, CharField, TextInput, DateTimeInput
from django.contrib.auth.models import User
# from django.db.models import DateTimeField, CharField

# from mon_ghs.MinimalSplitDateTimeMultiWidget import MinimalSplitDateTimeMultiWidget
# from mon_ghs.widgets import BootstrapDateTimePickerInput
from parametres.models import Symptome, Abonnement
from .models import Patient, Rdv, Payment


class PatientForm(ModelForm):
    dob = DateTimeInput(attrs={
        'class': 'form-control dateimepicker',
    })
    class Meta:
        model=Patient
        fields=[
            'genre',
            'dob',
            'poids',
            'groupe_sanguin',
            'telephone1',
            'image',
            'details',
        ]

class PatientEditForm(ModelForm):
    dob = DateTimeInput(attrs={
        'class': 'form-control dateimepicker',
    })
    class Meta:
        model=Patient
        fields=[
            'genre',
            'dob',
            'poids',
            'groupe_sanguin',
            'telephone1',
            'telephone2',
            'adresse',
            'image',
            'details',
        ]

class PaymentForm(ModelForm):
    # patient=ModelChoiceField(queryset=Patient.objects.all(),empty_label="Patient", to_field_name="user_id")
    abonnement = ModelChoiceField(queryset=Abonnement.objects.all(), empty_label="Abonnement")
    class Meta:
        model= Payment
        fields = [
            'abonnement',
        ]

class rdvForm(ModelForm):
    # patient=ModelChoiceField(queryset=Patient.objects.all(),empty_label="Patient", to_field_name="user_id")
    symptomes = ModelMultipleChoiceField(queryset=Symptome.objects.all(), widget=CheckboxSelectMultiple)
    date_rdv = DateInput()
    class Meta:
        model=Rdv
        # widgets = {
        #     'date_rdv': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%YT%H:%M'),
        # }
        fields=[
            'date_rdv',
            'poids',
            'symptomes',
            'details'
        ]
    # def __init__(self, *args, **kwargs):
    #     super(rdvForm, self).__init__(*args, **kwargs)
    #     # input_formats to parse HTML5 datetime-local input to datetime field
    #     self.fields['date_rdv'].input_formats = ('%d/%m/%YT%H:%M',)

class EditRdvForm(ModelForm):
    # patient=ModelChoiceField(queryset=Patient.objects.all(),empty_label="Patient", to_field_name="user_id")
    symptomes = ModelMultipleChoiceField(queryset=Symptome.objects.all(), widget=CheckboxSelectMultiple)
    # date_rdv = DateInput()
    class Meta:
        model=Rdv
        # widgets = {
        #     'date_rdv': DateInput(attrs={'type': 'datetime-local'}, format='%d/%m/%YT%H:%M'),
        # }
        fields=[
            'date_rdv',
            'poids',
            'symptomes',
            'details'
        ]
    # def __init__(self, *args, **kwargs):
    #     super(EditRdvForm, self).__init__(*args, **kwargs)
    #     # input_formats to parse HTML5 datetime-local input to datetime field
    #     self.fields['date_rdv'].input_formats = ('%d/%m/%YT%H:%M',)