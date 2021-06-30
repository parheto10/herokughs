from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from ghs_med.forms import ContactForm
from parametres.models import Faq


def about(request):
    return render(request, 'about.html')

def faq(request):
    faqs = Faq.objects.all()
    context = {
        'faqs':faqs
    }
    return render(request, 'parametres/faqs.html', context)

def contact(request):
    #today = timezone.now().date()
    queryset_list = Faq.objects.all()  # .order_by("-timestamp")
    paginator = Paginator(queryset_list, 12)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    titre = 'Formulaire de Contact'
    titre_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        from_email = form.cleaned_data.get("email")
        from_message = form.cleaned_data.get("message")
        from_telephone = form.cleaned_data.get("telephone")
        from_nom = form.cleaned_data.get("nom")
        sujet = 'Formulaire de Contact'
        to_email = ['settings.EMAIL_HOST_USER', 'parheto10@gmail.com', 'bebeto10toure@gmail.com']
        contact_message = "Message : %s\n\n Nom et Prenoms : %s\n\n Conatct : %s\n\n de : %s" % (
            from_message,
            from_nom,
            from_telephone,
            from_email
            )
        send_mail(
            sujet,
            contact_message,
            from_email,
            to_email,
            fail_silently=True,
        )
        messages.success(request, "Mail Envoyer Avec Success")
        return redirect("contact")
    else:
        context = {
            "form": form,
            "titre": titre,
            "titre_align_center": titre_align_center,
            "object_list": queryset,
            "annonces": "Ufra-Annonces",
            "page_request_var": page_request_var,
        }
        return render(request, "parametres/contact.html", context)

# Create your views here.
