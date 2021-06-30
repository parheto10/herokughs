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
from django_countries.fields import CountryField
# from phone_field.templatetags.phone import raw_phone
# from phonenumber_field.formfields import PhoneNumberField
#from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.modelfields import PhoneNumberField
from sorl.thumbnail import get_thumbnail

from parametres.models import Service, Hopital

def upload_images(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "images/" + ".jpeg"

GENRE = (
        ('H', 'HOMMME'),
        ('F', 'FEMME'),
    )

GRADE = (
        ('DR.', 'DOCTEUR'),
        ('MED.', 'MEDECIN'),
        ('INF.', 'INFIRMIER(E)'),
        ('AIDE', 'AIDE SOIGNANT(E)'),
        ('SECRETAIRE', 'SECRETAIRE'),
    )

class Personnel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=250, verbose_name="MATRICULE", unique=True)
    genre = models.CharField(max_length=10, verbose_name="GENRE", choices=GENRE, default="H")
    grade = models.CharField(max_length=50, choices=GRADE)
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    telephone1 = models.CharField(max_length=50, verbose_name="TELEPHONE 1")
    telephone2 = models.CharField(max_length=50, verbose_name="TELEPHONE 2", blank=True)
    adresse = models.CharField(max_length=255, verbose_name="ADRESSE", blank=True)
    bio = models.TextField(blank=True, null=True)
    # status = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to="upload_image_avatar", blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def Docteur(self):
        if self.user.last_name or self.user.first_name:
            return '%s %s (%s)' %(self.user.last_name, self.user.first_name, self.service.nom)
        else:
            return self.user.username

    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        if self.user.last_name or self.user.first_name:
            return '%s %s' %(self.user.last_name, self.user.first_name)
        else:
            #return self.user.username
            return "{}".format(self.user.username)


    def save(self, force_insert=False, force_update=False):
        self.user.last_name = self.user.last_name.upper()
        self.user.first_name = self.user.first_name.upper()
        self.adresse = self.adresse.upper()
        super(Personnel, self).save(force_insert, force_update)

    def thumb(self):
        if self.avatar:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.avatar.url)
        else:
            return "Aucune photo"

    thumb.short_description = 'Avatar'

    class Meta:
        verbose_name_plural = "PERSONNELS"
        verbose_name = "personnel"
        ordering = ('-add_le', '-update_le')