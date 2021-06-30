#from datetime import date
from dateutil import relativedelta
import time
import datetime
from datetime import datetime, date
from datetime import timedelta
import calendar
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic

from parametres.models import Symptome, Abonnement
from .forms import PatientForm, rdvForm, PaymentForm, EditRdvForm, PatientEditForm
from ghs_med.forms import UserForm
from .models import Patient, Rdv, Payment
from .utils import Calendar

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(generic.ListView):
    model = Rdv
    template_name = 'patients/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def calendrier(request):
    # patient = Patient.objects.get(user_id=request.user.id)
    # rdvs = Rdv.objects.all().filter(patient=patient)
    return render(request, 'patients/calendar.html', {})


def is_patient(user):
    return user.groups.filter(name='PATIENTS').exists()

def p_dashboard(request):
    patient = Patient.objects.all().filter(user_id=request.user.id)
    if patient:
        return redirect('dashboard')
    else:
        return render(request, '/')

# @login_required(login_url='connexion')
def edit_patient(request, id=None):
    user = Patient.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Patient, id=id)
    form = PatientEditForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user_id = user.id
        instance.save()
        # instance.save()
        messages.success(request, "Modification Effectuée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:pepinieres'))

    context = {
        "user":user,
        "instance": instance,
        "form": form,
    }
    return render(request, "patients/edit_dashboard.html", context)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def patient_dashboard(request):
    patient= Patient.objects.get(user_id=request.user.id)
    rdvs=Rdv.objects.all().filter(patient=patient).order_by("-add_le", "-update_le")
    today = datetime.now()
    age = today.year - patient.dob.year
    context={
    'patient':patient,
    'rdvs': rdvs,
    'age': age,
    }
    return render(request,'patients/patient-dashboard.html',context=context)

def add_patient(request):
    userForm=UserForm()
    patientForm=PatientForm()
    if request.method=='POST':
        userForm=UserForm(request.POST)
        patientForm=PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            password = userForm.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient=patient.save()
            print(patient)
            patient_group = Group.objects.get_or_create(name='PATIENTS')
            patient_group[0].user_set.add(user)
            patient = authenticate(username=user.username, password=password)
            dj_login(request, patient)
            # if next:
            #     return redirect(next)
            messages.success(request, "Inscription effectuée avec succès")
            return HttpResponseRedirect(reverse('patient:abonnement'))
    context = {
        'userForm': userForm,
        'patientForm': patientForm
    }
    return render(request,'patients/add_patient.html',context=context)

# def checkout(request):
#     patient = Patient.objects.get(user_id=request.user.id)
#     context = {
#         'patient': patient,
#     }
#     return render(request, 'patients/paiement.html', context)
@login_required(login_url='connexion')
@user_passes_test(is_patient)
def rdv_patient(request):
    form=rdvForm()
    patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    mydict={'form':form,'patient':patient}
    if request.method=='POST':
        form=rdvForm(request.POST)
        if form.is_valid():
            rdv=form.save(commit=False)
            rdv.patient=Patient.objects.get(user_id=request.user.id)
            rdv.save()
        return HttpResponseRedirect(reverse('patient:dashboard'))
    return render(request,'patients/calendar1.html',context=mydict)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def edit_rdv(request, id=None):
    instance = get_object_or_404(Rdv, id=id)
    form = EditRdvForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "RDV Modifié avec succès")
        return HttpResponseRedirect(reverse('patient:dashboard'))
    context = {
        "instance": instance,
        "form":form
    }
    return render(request, "patients/rdv_edit.html", context)
# def rdv_patient(request):
#     patient=Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
#     paiement = Payment.objects.filter(patient_id=request.user.id)
#     form = rdvForm(request.POST or None)
#     if request.method=='POST' and form.is_valid():
#         date = form.cleaned_data['date_rdv']
#         detail = form.cleaned_data['details']
#         p = form.cleaned_data['poids']
#         pat= patient.id
#         rdv = Rdv.objects.create(
#             date_rdv=date,
#             poids=p,
#             details=detail,
#             patient_id=pat,
#         )
#         for symp in form.cleaned_data['symptomes']:
#             rdv.save(symp)
#
#             # rdv=form.save(commit=False)
#             # rdv.patient=Patient.objects.get(user_id=request.user.id)
#             # rdv_symptomes = Symptome.objects.filter(symptome__in=symp)
#             # rdv.symptomes.set(rdv_symptomes)
#             # rdv.patient.nb_consultation = (patient.nb_consultation) - 1
#             # rdv.is_valid=False
#             # rdv.save()
#         return HttpResponseRedirect(reverse('patient:dashboard'))
#     mydict = {'form': form, 'patient': patient, 'paiement': paiement}
#     return render(request,'patients/rdv.html',context=mydict)

@login_required(login_url='connexion')
@user_passes_test(is_patient)
def abonnement(request):
    paymentForm = PaymentForm()
    patient=Patient.objects.get(user_id=request.user.id)
    abonnements = Abonnement.objects.all()

    if request.method=='POST':
        paymentForm=PaymentForm(request.POST)
        if paymentForm.is_valid():
            payment=paymentForm.save(commit=False)
            payment.patient = Patient.objects.get(user_id=request.user.id)
            payment.patient.is_abonne = True
            payment.patient.nb_consultation = payment.abonnement.consultation
            payment.save()
        return HttpResponseRedirect(reverse('patient:rdv'))
    mydict = {
        'paymentForm': paymentForm,
        'patient': patient,
        'abbonements':abonnements
    }
    return render(request,'patients/paiement.html',context=mydict)