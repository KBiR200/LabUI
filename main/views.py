from django.shortcuts import render
from reports.models import Report, Tasks
from chem.settings import BASE_DIR
# Create your views here.



def home(request):
    return render(request, 'index.html')


def signin(request):
    return render(request, 'signin.html')


def admin(request):
    tasks = Tasks.objects.all()
    reports = Report.objects.filter(author=request.user)
    return render(request, 'cards.html', {'reports': reports, 'tasks':tasks})