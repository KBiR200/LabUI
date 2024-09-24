from django.shortcuts import render, redirect
from main.models import Machine
from reports.models import Report, Records, Tasks
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from chem.settings import BASE_DIR
from django.contrib.auth.decorators import login_required


# report view function
@login_required
def new_report(request):
    test_name= 'Change the Name'
    r = Report.objects.create(title=test_name)
    r.author.set([request.user])
    print(r.id)
    return redirect("report", pk=r.id)


@login_required
def update_report(request,pk):
    rep = get_object_or_404(Report, id=pk)
    # check user 
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        return HttpResponseForbidden("You are not allowed to edit this form.")
    task = Tasks.objects.filter(assigned=request.user)
    if request.method == "POST":
        try:
            t = request.POST['task']
            print(f'the task is {t}')
            rep.task = get_object_or_404(Tasks, id=t)
            rep.save()
        except:
            print('something off')
    return render(request, 'reports.html',{'machines': Machine.objects.all(), 'rep':rep, 'tasks':task})


@login_required
def show_report(request, pk):
    rep = get_object_or_404(Report, id=pk)
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        return HttpResponseForbidden("You are not allowed to edit this form.")
    related_records = rep.reports_records.all()
    for i in related_records:
        print(i.data)
    return render(request, 'show_report.html', {'records':related_records, 'reports':rep})

# record view function

@login_required
def save_record(request, pk):
    if request.method == 'POST':
        try:
            print('Processing POST request')
            form_data = {}
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken' and key != 'machine_id':  # Ignore the CSRF token field and machine ID 
                    form_data[key] = value
            final_data = {"values": form_data}
            print('Form Data:', final_data)
            machine_id = request.POST.get('machine_id')
            print(f'Machine ID: {machine_id}')
            report = Report.objects.get(id=pk)
            machine = Machine.objects.get(id=machine_id)
            record = Records.objects.create(data=final_data)
            record.report.add(report)
            record.machine.add(machine)
            record.save()
            return JsonResponse({'success': True, 'data': form_data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    


# Tasks view function

@login_required
def create_task(request):
    
    users = User.objects.all()  # Fetch all users
    if request.method == 'POST':
        title = request.POST['title']
        data = request.POST.get('data', '')
        
        task = Tasks.objects.create(creator=request.user, data=data, title = title)
        # task.signed.set(assigned_users)
        task.save()
        print(f'task: {title} is created')
        return redirect('control')  # Redirect to a task list or another page after creation
    
    return render(request, 'task.html', {'users': users})

@login_required
def show_task(request, pk):
    task = get_object_or_404(Tasks, id=pk)
    print(task.assigned.all().count())
    print(task.title)
    return redirect('control')

@login_required
def accept_task(request, pk):
    print(f"Task ID = {pk}")
    task = get_object_or_404(Tasks, id=pk)
    task.assigned.add(request.user)
    task.status = 1
    task.save()
    print("u are assigned")
    return redirect('control')

@login_required
def submit_task(req, pk):
    print(f"Task ID = {pk}")
    task = get_object_or_404(Tasks, id=pk)
    task.status = 2
    task.save()
    print('task is handed')
    return redirect('control')