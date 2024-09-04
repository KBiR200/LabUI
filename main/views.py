from django.shortcuts import render
from reports.models import Report
from chem.settings import BASE_DIR
# Create your views here.



def home(request):
    return render(request, 'index.html')


def signin(request):
    return render(request, 'signin.html')

def post(request):
    return render(request, 'reports.html')

def admin(request):

    reports = Report.objects.all()
    return render(request, 'cards.html', {'reports': reports})