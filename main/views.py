from django.shortcuts import render
from reports.models import Report, Tasks
from chem.settings import BASE_DIR
# Create your views here.



def home(request):
    return render(request, 'index.html')


def signin(request):
    return render(request, 'login.html')


def dashboard(request):
    tasks = Tasks.objects.filter(status=1, assigned=request.user).order_by('-created_at')
    report = Report.objects.filter(author=request.user)
    for i in report:
        print(i.pk)
        print(i.title)
    context = {
        'tasks': tasks,
        'reports':report
    }
    return render(request, 'dahsboard copy.html', context)

def new_requests(request):
    tasks = Tasks.objects.filter(status=0).order_by('-created_at')
    return render(request, 'new_tasks.html',{'tasks':tasks})