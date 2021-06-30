from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from .forms import LoginForm
# from patients.models import Patient
# from docteurs.models import Docteur
# from .forms import UserForm, LoginForm
# from patients.forms import PatientForm, rdvForm
# from patients.models import Patient, Rdv
# from personnels.models import Personnel

def loggout(request):
    logout(request)
    return redirect("index")

def index(request):
    return render(request, 'index.html', {})

def connexion(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            #utilisateur valide et actif(is_active=True)
            #"request.user == user"
            dj_login(request, user)
            group = request.user.groups.filter(user=request.user)[0]
            if group.name == "PATIENTS":
                messages.success(request, "Bienvenus : {}".format(username))
                return HttpResponseRedirect(reverse('patient:dashboard'))
            elif group.name == "DOCTEURS":
                messages.success(request, "Bienvenus : {}".format(username))
                return HttpResponseRedirect(reverse('docteurs:dashboard'))
            else:
                messages.error(request, "Désolé vous n'estes pas encore enregistrer dans notre Sytème")
                return HttpResponseRedirect(reverse('connexion'))
        else:
            request.session['invalid_user'] = 1 # 1 == True
    return render(request, 'login.html', {'login_form': login_form})