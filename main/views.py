from django.shortcuts import render, redirect
from reports.models import Report, Tasks
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from chem.settings import BASE_DIR
# Create your views here.



def home(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contactus.html')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('control')  # Redirect to a success page.
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def dashboard(request):
    tasks = Tasks.objects.filter(status=1, assigned=request.user).order_by('-created_at')
    tasks_history = Tasks.objects.filter(assigned=request.user).order_by('-created_at')
    report = Report.objects.filter(author=request.user)
    context = {
        'tasks': tasks,
        'tasks_history': tasks_history,
        'reports':report
    }
    return render(request, 'dahsboard copy.html', context)

def new_requests(request):
    tasks = Tasks.objects.filter(status=0).order_by('-created_at')
    return render(request, 'new_tasks.html',{'tasks':tasks})