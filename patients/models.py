# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.db import models
import datetime
import time

from django.urls import reverse
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField
from sorl.thumbnail import get_thumbnail

from parametres.models import Symptome, Service, Abonnement


def upload_images(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "images/" + ".jpeg"

def images_assure(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "assure/" + ".jpeg"

GENRE = (
        ('H', 'HOMMME'),
        ('F', 'FEMME'),
    )

EXAMENS = (
    ("AUCUN", "AUCUN"),
    ("BIOLOGIE", "BIOLOGIE"),
    ("RADIOLOGIE", "RADIOLOGIE"),
)

ALERTS = (
    ("APPEL", "APPEL"),
    ("EMAIL", "EMAIL"),
    ("SMS", "SMS"),
)

GROUPE_SANGUIN = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'A-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=10, verbose_name="GENRE", choices=GENRE, default="H")
    dob = models.DateField(verbose_name="Date de Naissance")
    poids = models.DecimalField(max_digits=3, decimal_places=1)
    groupe_sanguin = models.CharField(max_length=3, verbose_name="GROUPE SANGUIN", choices=GROUPE_SANGUIN, default="A+")
    telephone1 = models.CharField(max_length=50, verbose_name="TELEPHONE 1")
    telephone2 = models.CharField(max_length=50, verbose_name="TELEPHONE 2", blank=True)
    adresse = models.CharField(max_length=255, verbose_name="ADRESSE", blank=True, null=True)
    image = models.ImageField(upload_to="upload_image", blank=True, null=True)
    details = models.TextField(verbose_name="Historique Médical")
    nb_consultation = models.PositiveIntegerField(default=0, verbose_name="NOMBRE DE CONSULTATION")
    is_abonne = models.BooleanField(default=False, verbose_name="ABONNEMENT")

    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "PATIENTS"
        verbose_name = "patient"
        ordering = ["-add_le"]

    def Patient(self):
        return '%s %s' %(self.user.last_name, self.user.first_name)

    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        if self.user.last_name or self.user.first_name:
            return '%s %s' %(self.user.last_name, self.user.first_name)
        else:
            return self.user.username

    def thumb(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
        else:
            return "Aucune photo"

    thumb.short_description = 'Image'

    def get_absolute_url(self):
        #return reverse('patient:dashboard', args=[self.id])
        return reverse("patient:profile", kwargs={"username": self.user.username})
        # return reverse('patient:dashboard', kwargs={"username":self.user.username}

class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='abonnement_patient')
    abonnement = models.ForeignKey(Abonnement, on_delete=models.CASCADE, related_name='abonnement_formule', default=1)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        unique_together = ['patient', 'abonnement']

    def __str__(self):
        return str(self.patient.user.username)

class Rdv(models.Model):
    code = models.CharField(max_length=150, blank=True, verbose_name='CODE RDV', help_text="LE CODE RDV EST GENERE AUTOMATIQUEMENT")
    date_rdv =  models.DateTimeField(verbose_name="DATE DU RDV")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rdv_patient')
    poids = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    taille = models.PositiveIntegerField(default=0, verbose_name="Taille(cm)")
    ta = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="TENSION ARTERIELLE(TA)", blank=True, null=True)
    poults = models.PositiveIntegerField(default=0)
    systolique = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)#models.PositiveIntegerField(default=0)
    diastolique = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)#models.PositiveIntegerField(default=0)
    symptomes = models.ManyToManyField(Symptome)
    nb_rdv = models.PositiveIntegerField(default=0)
    alert = models.CharField(max_length=100, choices=ALERTS, default="EMAIL", verbose_name="ALERT RDVS")
    last_examen = models.CharField(max_length=25, choices=EXAMENS, verbose_name="DERNIERS EXAMENS DES DERNIERS MOIS", default="BIOLOGIE")
    details = models.TextField(help_text="Préciser les details de la dernieres Consultation SVP", blank=True, null=True)
    diagnostique = models.TextField(help_text="Diagnostique Finale", blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-add_le', '-update_le']

    def Patient(self):
        return '%s %s' % (self.patient.user.last_name, self.patient.user.first_name)

    def __str__(self):
        return 'Rdv de %s le %s' %(self.patient, self.date_rdv)

    def clean(self):
        # numerotation automatique
        if not self.id:
            tot = Rdv.objects.count()
            numero = tot + 1
            madate = datetime.date.today()
            self.code = "%s-%s" % (numero, datetime.date.strftime(madate, '%d/%m/%Y'))
            if self.diastolique and self.systolique:
                self.ta = (self.diastolique + self.systolique) / 2

    class Meta:
        verbose_name_plural = "RDVS"
        verbose_name = "rdv"
        unique_together = ['patient', 'date_rdv']

    def get_absolute_url(self):
        return reverse('patient:rdv', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('patient:rdv')
        return f'<a href="{url}"> {self.code} </a>'