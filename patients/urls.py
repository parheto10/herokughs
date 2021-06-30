from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from .views import (
    patient_dashboard,
    add_patient,
    rdv_patient,
    CalendarView,
    abonnement,
    edit_rdv,
    edit_patient
    # profile_patient,
    # profile_setting

)

app_name= 'patient'

urlpatterns = [
    # Patient
    path('dashboard/', patient_dashboard, name='dashboard'),
    path('abonnement/', abonnement, name='abonnement'),
    path('calendrier/', CalendarView.as_view(), name='calendrier'),
    # path('settings/', profile_setting, name='settings'),
    path('inscription/', add_patient, name="inscription"),
    path('edit_rdv/<int:id>', edit_rdv, name="edit_rdv"),
    path('rdv/', rdv_patient, name="rdv"),
    path('edit_patient/<int:id>', edit_patient, name="edit_patient"),

]