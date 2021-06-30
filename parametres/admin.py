from django.contrib import admin

from .models import Symptome, Abonnement, Hopital, Service, Pathologie, Faq

class FaqAdmin(admin.ModelAdmin):
    list_display = ['question']
    list_display_links = ["question", ]
    prepopulated_fields = {'slug': ('question',)}

admin.site.register(Abonnement)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Hopital)
admin.site.register(Pathologie)
admin.site.register(Service)
admin.site.register(Symptome)

# Register your models here.
