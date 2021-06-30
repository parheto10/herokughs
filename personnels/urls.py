from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from .views import (
    docteur_dashboard,
    rdv_dashboard,
    patient_dashboard,
    add_docteur,
    edit_rdv,
)

app_name= 'docteurs'

urlpatterns = [
    # Patient
    path('add_docteur/', add_docteur, name='add_docteur'),
    path('dashboard/', docteur_dashboard, name='dashboard'),
    path('rdv_dashboard/', rdv_dashboard, name='rdv_dashboard'),
    path('edit_rdv/<int:id>', edit_rdv, name='edit_rdv'),
    path('patient_dashboard/', patient_dashboard, name='patient_dashboard'),
]