from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

User = get_user_model()
non_allowed_username = ["abc", "123", "admin1", "admin12"]

class LoginForm(forms.Form):
    username = forms.CharField(label="Nom Utilisateur")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password"}), label="Mot de Passe")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists:
            raise forms.ValidationError("Utilisateur Invalide !!!")
        return username

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['last_name','first_name','username', 'email', 'password']


#for contact us page
class ContactForm(forms.Form):
    nom = forms.CharField(label='Nom et Prenoms')
    telephone = forms.CharField(label='Contacts')
    email = forms.EmailField()
    message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
