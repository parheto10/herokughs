from .models import Patient

def inscription(request):
    return {'inscription' : Patient(request)}

