from django.shortcuts import render
from reports.models import Report, Tasks
from chem.settings import BASE_DIR
# Create your views here.



def home(request):
    return render(request, 'index.html')


def signin(request):
    return render(request, 'login.html')


def control(request):
    tasks = Tasks.objects.filter(status=1, assigned=request.user)
    reports = Report.objects.filter(status=0,author=request.user).order_by('-date_added')
    return render(request, 'cards.html', {'reports': reports, 'tasks':tasks})

def new_requests(request):
    tasks = Tasks.objects.filter(status=0)
    return render(request, 'new_tasks.html',{'tasks':tasks})