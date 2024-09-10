from django.shortcuts import render, redirect
from main.models import Machine
from reports.models import Report, Records, Tasks
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from chem.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def update_report(request,pk):
    r= Report.objects.all()
    rep = get_object_or_404(Report, id=pk)
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        return HttpResponseForbidden("You are not allowed to edit this form.")
    return render(request, 'reports.html',{'machines': Machine.objects.all(), 'rep':rep})

def new_report(request):
    # r= Report.objects.all()
    # rep = get_object_or_404(Report, id=pk)
    # if request.user.id not in list(rep.author.values_list("id", flat=True)):
    #     return HttpResponseForbidden("You are not allowed to edit this form.")
    return render(request, 'reports.html',{'machines': Machine.objects.all()})


def save_record(request, pk):
    if request.method == 'POST':
        try:
            print('Processing POST request')
            form_data = {}

            # Loop through POST data and add the form fields to the dictionary
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken' and key != 'machine_id':  # Ignore the CSRF token field and machine ID 
                    form_data[key] = value
            final_data = {"values": form_data}
            print('Form Data:', final_data)
            machine_id = request.POST.get('machine_id')
            print(f'Machine ID: {machine_id}')
            report = Report.objects.get(id=pk)
            machine = Machine.objects.get(id=machine_id)

            # Create the Record object first (without Many-to-Many relationships)
            record = Records.objects.create(data=final_data)
            record.report.add(report)
            record.machine.add(machine)

            # Save the record
            record.save()
            return JsonResponse({'success': True, 'data': form_data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    

def show_report(request, pk):
    rep = get_object_or_404(Report, id=pk)
    related_records = rep.reports.all()
    for i in related_records:
        print(i.data)
    return render(request, 'show_report.html', {'records':related_records, 'reports':rep})


def create_task_view(request):
    users = User.objects.all()  # Fetch all users
    if request.method == 'POST':
        title = request.POST['title']
        status = request.POST['status']
        assigned_users = request.POST.getlist('assigned_users')
        data = request.POST.get('data', '')
        
        task = Tasks.objects.create(initiator=request.user, status=status, data=data)
        task.signed.set(assigned_users)
        task.save()
        return redirect('admin.html')  # Redirect to a task list or another page after creation
    
    return render(request, 'task.html', {'users': users})