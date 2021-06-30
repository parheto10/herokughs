from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from dateutil import relativedelta
import time
import datetime
from .forms import DocteurForm
from ghs_med.forms import UserForm


def add_docteur(request):
    userForm=UserForm()
    doctorForm=DocteurForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=UserForm(request.POST)
        docteurForm=DocteurForm(request.POST,request.FILES)
        if userForm.is_valid() and docteurForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            docteur=doctorForm.save(commit=False)
            docteur.user=user
            docteur=docteur.save()
            docteur_group = Group.objects.get_or_create(name='DOCTEURS')
            docteur_group[0].user_set.add(user)
        return HttpResponseRedirect('/')
    return render(request,'docteurs/add_docteur.html',context=mydict)

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

# from ghs.forms import LoginForm
# from patients.models import Patient
from .models import Personnel
from ghs_med.forms import UserForm, LoginForm
from patients.forms import PatientForm, rdvForm, EditRdvForm
from patients.models import Patient, Rdv
from personnels.models import Personnel
from .forms import EditRdvAdminForm

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
            if group.name == "DOCTEURS":
                messages.success(request, "Bienvenus : {}".format(username))
                return HttpResponseRedirect(reverse('docteurs:dashboard'))
            else:
                messages.error(request, "Désolé vous n'estes pas encore inscris comme docteur")
                return HttpResponseRedirect(reverse('connexion'))
        else:
            request.session['invalid_user'] = 1 # 1 == True
    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)

def is_docteur(user):
    return user.groups.filter(name='DOCTEURS').exists()

def p_dashboard(request):
    docteur = Personnel.objects.all().filter(user_id=request.user.id)
    if docteur:
        return redirect('')
    else:
        return render(request, '/')


@login_required(login_url='connexion')
@user_passes_test(is_docteur)
def docteur_dashboard(request):
    docteur= Personnel.objects.get(user_id=request.user.id)
    docteurs = Personnel.objects.all()
    rdvs= Rdv.objects.all().order_by('-add_le', '-update_le')
    last_rdvs_valid= Rdv.objects.all().order_by('-add_le', '-update_le')[:10]
    nb_rdvs=Rdv.objects.all().count()
    patients = Patient.objects.all()
    nb_patients = Patient.objects.all().count()
    today = datetime.datetime.now()
    #age = today.year - docteur.dob.year
    context={
    'docteur':docteur,
    'docteurs':docteurs,
    'rdvs': rdvs,
    'last_rdvs_valid': last_rdvs_valid,
    'nb_rdvs':nb_rdvs,
    'patients':patients,
    'nb_patients':nb_patients,
    }
    return render(request,'docteurs/dashboard.html',context=context)


@login_required(login_url='connexion')
@user_passes_test(is_docteur)
def rdv_dashboard(request):
    rdvs= Rdv.objects.all().order_by('-add_le', '-update_le')
    context={
    'rdvs': rdvs,
    }
    return render(request, 'docteurs/rdvs.html', context=context)

def edit_rdv(request, id=None):
    instance = get_object_or_404(Rdv, id=id)
    form = EditRdvAdminForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        if instance.diastolique and instance.systolique:
            instance.ta = (instance.diastolique + instance.systolique) / 2
        instance.save()
        messages.success(request, "RDV Modifié avec succès")
        return HttpResponseRedirect(reverse('docteurs:rdv_dashboard'))
    context = {
        "instance": instance,
        "form":form
    }
    return render(request, "patients/rdv_edit.html", context)

@login_required(login_url='connexion')
@user_passes_test(is_docteur)
def patient_dashboard(request):
    patients= Patient.objects.all()
    context={
        'patients': patients,
    }
    return render(request, 'docteurs/patients.html', context=context)
# Create your views here.
