from django.contrib import admin

from .models import Patient, Rdv, Payment

admin.site.register(Patient)
admin.site.register(Payment)
admin.site.register(Rdv)

# Register your models here.
