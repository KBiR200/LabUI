from django.shortcuts import render, redirect
from main.models import Machine
from reports.models import Report, Records, Tasks, Records_attachment, Task_attachment
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from chem.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
import datetime

# report view function
@login_required(login_url='signin')
def new_report(request):
    test_name= f'Created: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    r = Report.objects.create(title=test_name)
    r.author.set([request.user])
    print(r.id)
    return redirect("report", pk=r.id)


@login_required(login_url='signin')
def update_report(request,pk):
    rep = get_object_or_404(Report, id=pk)
    # check user 
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        return HttpResponseForbidden("You are not allowed to edit this form.")
    task = Tasks.objects.filter(assigned=request.user, status=1)
    if request.method == "POST":
        try:
            t = request.POST['task']
            print(f'the task is {t}')
            rep.task = get_object_or_404(Tasks, id=t)
            rep.save()
        except:
            print('something off')
    return render(request, 'reports.html',{'machines': Machine.objects.all(), 'rep':rep, 'tasks':task})


@login_required(login_url='signin')
def show_report(request, pk):
    rep = get_object_or_404(Report, id=pk)
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        return HttpResponseForbidden("You are not allowed to edit this form.")
    related_records = rep.reports_records.all().prefetch_related('attachments')
    for i in related_records:
        print(i.data)
    return render(request, 'show_report.html', {'records':related_records, 'reports':rep})

# record view function

@login_required(login_url='signin')
def save_record(request, pk):
    if request.method == 'POST':
        try:
            print('Processing POST request')
            form_data = {}
            for key, value in request.POST.items():

                if key != 'csrfmiddlewaretoken' and key != 'machine_id' and key!= "attachment":  # Ignore the CSRF token field and machine ID 
                    print(key)
                    form_data[key] = value
            form_attachment = request.FILES.getlist('attachment')
            print(form_attachment)
            final_data = {"values": form_data}
            # print('Form Data:', final_data)
            machine_id = request.POST.get('machine_id')
            # print(f'Machine ID: {machine_id}')
            report = Report.objects.get(id=pk)
            machine = Machine.objects.get(id=machine_id)
            record = Records.objects.create(data=final_data)
            record.report.add(report)
            record.machine.add(machine)
            record.save()
            # print(record.id)
            for i in form_attachment:
                print(i)
                r= Records_attachment.objects.create(record=record, attachment=i)
                print(r.id)

            return JsonResponse({'success': True, 'data': form_data})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    


# Tasks view function

@login_required(login_url='signin')
def create_task(request):
    
    users = User.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        data = request.POST.get('data', '')
        due_date = request.POST['due_date']
        form_attachment = request.FILES.getlist('attachment')
        task = Tasks.objects.create(creator=request.user, data=data, title = title, due_date=due_date)
        # task.signed.set(assigned_users)
        task.save()
        print(f'task: {title} is created')
        print(form_attachment)
        for i in form_attachment:
            print(i)
            r= Task_attachment.objects.create(task=task, attachment=i)
        return redirect('control')
    
    return render(request, 'task.html', {'users': users})

@login_required(login_url='signin')
def show_task(request, pk):
    task = get_object_or_404(Tasks, id=pk)
    print(task.assigned.all().count())
    print(task.title)
    return render(request, 'task_view.html', {"task":task})

@login_required(login_url='signin')
def accept_task(request, pk):
    print(f"Task ID = {pk}")
    task = get_object_or_404(Tasks, id=pk)
    task.assigned.add(request.user)
    task.status = 1
    task.save()
    print("u are assigned")
    return redirect('control')

@login_required(login_url='signin')
def submit_task(req, pk):
    print(f"Task ID = {pk}")
    task = get_object_or_404(Tasks, id=pk)
    task.status = 2
    task.save()
    print('task is handed')
    return redirect('control')