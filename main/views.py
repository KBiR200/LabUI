from enum import member
import profile
from django.shortcuts import render, redirect
from main.models import Project, Laberatory, Machine, Team, Machine_Category, UserProfile
from reports.models import Report, Tasks
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from chem.settings import BASE_DIR
# Create your views here.



def home(request):
    # return render(request, 'index.html')
    return redirect('control')

def contact(request):
    return render(request, 'contactus.html')

def teams(request):
    team = Team.objects.filter(members = request.user)
    return render(request, 'teams15.html',{'team': team})

# def lab(request):
#     labs = Laberatory.objects.all()
#     machines = Machine.objects.all()

#     return render(request, 'lab/lab.html', {'labs': labs, 'machines': machines})



# def machine(request, pk):
#     machine = get_object_or_404(Machine, id=pk)
#     return render(request, 'lab/machine.html', {'machine': machine})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = request.POST.get('remember_me', False)
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Set session expiry based on remember_me
                if not remember_me:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                else:
                    # Session expires after 2 weeks (in seconds)
                    request.session.set_expiry(1209600)
                
                # Redirect to success page
                return redirect('control')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            # Get specific error messages from the form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form = AuthenticationForm()
    
    return render(request, 'signin15.html', {'form': form})

@login_required(login_url='signin')
def logout_view(request):
    logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def dashboard(request):
    print(request.user.groups.all())
    tasks = Tasks.objects.filter(status=1, assigned=request.user).order_by('-created_at')
    new_tasks = Tasks.objects.filter(status=0).order_by('-created_at')
    tasks_history = Tasks.objects.filter(assigned=request.user).order_by('-created_at')
    report = Report.objects.filter(author=request.user)
    context = {
        'tasks': tasks,
        'new_tasks': new_tasks,
        'tasks_history': tasks_history,
        'reports':report
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='signin')
def userprofile(request):

    return render(request, 'profile.html')


@login_required(login_url='signin')
def new_requests(request):
    supervisors = User.objects.filter(userprofile__in=request.user.userprofile.supervisor.all())
    tasks = Tasks.objects.filter(
        Q(creator=request.user) | Q(creator__in=supervisors),
        status=0,
        ).order_by('-created_at')
    print(len(supervisors))
    return render(request, 'new_requests.html',{'tasks':tasks})


login_required(login_url='signin')
def password_change(request):
    if request.method == 'POST':
        user = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('password_change')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('password_change')
        print(f"""
        Old password: {old_password}    
        New password: {new_password}""")
        # user.set_password(new_password)
        # user.save()
        messages.success(request, "Password changed successfully.")
        return redirect('signin')

    return render(request, 'passchange.html')



def error_404(request):
    context = {
            'error_type': 'permission',
            'error_code': '500',
            'error_title': 'Access Denied',
            'error_message': 'You are not the Laboratory Coordinator (LC) so you cannot access this page.',
            'user': request.user,
            'required_role': 'Laboratory Coordinator (LC)',
            'current_role': request.user,
        }
    return render(request, 'error/error.html',context=context, status=500)