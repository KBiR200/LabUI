from django.shortcuts import render, redirect
from main.models import Machine
from django.views.decorators.csrf import csrf_exempt
from reports.models import Report, Records, Tasks, Records_attachment, Task_attachment
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from chem.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
import datetime, json

"""--------------------- Reports ---------------------"""

@login_required(login_url='signin')
def reports(request):

    return render(request, 'reports/reports15.html')

# report view function
@login_required(login_url='signin')
def new_report(request, task_id):
    test_name= f'Created: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    task = get_object_or_404(Tasks, id=task_id)
    print(task)
    if request.method == 'POST':
        title = request.POST['title']
        # data = request.POST.get('data', '')
        # due_date = request.POST['due_date']
        # form_attachment = request.FILES.getlist('attachment')
        r = Report.objects.create(title=title, task=task)
        r.author.set([request.user])
        # task = Tasks.objects.create(creator=request.user, data=data, title = title, due_date=due_date)
        r.save()
        print(f'report: {title} is created with ID {r.id}')
        # for i in form_attachment:
        #     print(i)
        #     tt= Task_attachment.objects.create(task=task, attachment=i)
        return redirect('update_report', report_id=r.id)

    return render(request,"reports/report_create15.html", {"pk":task.id})


@login_required(login_url='signin')
def update_report(request,report_id):
    test_name= f'Created: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    report = get_object_or_404(Report, id=report_id)
    related_records = report.reports_records.all().prefetch_related('attachments')
    print(report)
    print(related_records)
    if request.method == 'POST':
        title = request.POST['title']
        # data = request.POST.get('data', '')
        # due_date = request.POST['due_date']
        # form_attachment = request.FILES.getlist('attachment')
        report.title = title
        # r.author.set([request.user])
        # task = Tasks.objects.create(creator=request.user, data=data, title = title, due_date=due_date)
        report.save()
        print(f'report: {title} is created with ID {report.id}')
        # for i in form_attachment:
        #     print(i)
        #     tt= Task_attachment.objects.create(task=task, attachment=i)
        return redirect('show_report', pk=report.id)

    return render(request,"reports/report_update.html", {"pk":report.id, "report":report, 'records':related_records})


@login_required(login_url='signin')
def show_report(request, pk):
    rep = get_object_or_404(Report, id=pk)
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        return HttpResponseForbidden("You are not allowed to edit this form.")
    related_records = rep.reports_records.all().prefetch_related('attachments')
    for i in related_records:
        print(i.data)
    return render(request, 'reports/report_view15.html', {'records':related_records, 'report':rep})

@login_required(login_url='signin')
def submit_report(req, pk):
    print(f"Task ID = {pk}")
    rep = get_object_or_404(Report, id=pk)
    rep.status = 2
    rep.save()
    print('report is submited')
    return redirect('show_report', pk=rep.id)

# record view function
"""--------------------- Records ---------------------"""

# @login_required(login_url='signin')
# def old(request, pk):
#     if request.method == 'POST':
#         try:
#             print('Processing POST request')
#             form_data = {}
#             for key, value in request.POST.items():
#                 print(key, value)
#                 if key != 'csrfmiddlewaretoken' and key != 'machine_id' and key!= "attachment":  # Ignore the CSRF token field and machine ID 
#                     print(key)
#                     form_data[key] = value
#             form_attachment = request.FILES.getlist('attachment')
#             print(form_attachment)
#             final_data = {"values": form_data}
#             machine_id = request.POST.get('machine_id')
#             report = Report.objects.get(id=pk)
#             machine = Machine.objects.get(id=machine_id)
#             record = Records.objects.create(data=final_data)
#             record.report.add(report)
#             record.machine.add(machine)
#             record.save()
#             for i in form_attachment:
#                 print(i)
#                 r= Records_attachment.objects.create(record=record, attachment=i)
#                 print(r.id)
#             return JsonResponse({'success': True, 'data': form_data})
#         except Exception as e:
#             return JsonResponse({'success': False, 'message': str(e)})
#     else:
#         return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def save_record(request, pk):
    if request.method == 'POST':
        try:
            # Retrieve the JSON string from POST data.
            # This should be a JSON array of record objects.
            records_json = request.POST.get("records_json", "[]")
            try:
                records_data = json.loads(records_json)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
            
            # Get attachments (if any)
            attachments = request.FILES.getlist('attachment')
            
            # Get the Report instance using the provided pk (e.g., from URL)
            report = Report.objects.get(id=pk)
            
            created_records = []
            
            # Process each record in the JSON array
            for record_obj in records_data:
                # Extract machine name and parameters from the JSON record
                machine_name = record_obj.get("machine", "")
                parameters = record_obj.get("parameters", {})
                
                # Build final data structure to store in the Records model
                # (Here we wrap machine and parameters into a single dict.)
                final_data = {"machine": machine_name, "parameters": parameters}
                
                # Create a Records instance with the final_data
                record = Records.objects.create(data=final_data)
                
                # Associate the record with the report (assuming ManyToMany field)
                record.report.add(report)
                
                # Look up the Machine object based on the machine name.
                # (Assumes machine names are unique. Adjust lookup as needed.)
                try:
                    machine = Machine.objects.get(name="Rheology")
                    record.machine.add(machine)
                except Machine.DoesNotExist:
                    # If no matching machine is found, you might log or handle this case.
                    pass
                
                record.save()
                
                # Attach any uploaded files to this record.
                # (If attachments should only be applied to one record, adjust as needed.)
                for f in attachments:
                    Records_attachment.objects.create(record=record, attachment=f)
                
                created_records.append(record)
            
            # Return a JSON response with success and count of records created.
            print( JsonResponse({'success': True, 'records_created': len(created_records)}))
            return redirect('show_report', pk=pk)
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

"""--------------------- Tasks ---------------------"""

@login_required(login_url='signin')
def tasks(request):
    tasks = Tasks.objects.all().order_by('-created_at')
    new_tasks = Tasks.objects.filter(status=0).order_by('-created_at')
    tasks_history = Tasks.objects.filter(assigned=request.user).order_by('-created_at')
    report = Report.objects.filter(author=request.user)
    context = {
        'tasks': tasks,
        'new_tasks': new_tasks,
        'tasks_history': tasks_history,
        'reports':report
    }
    
    return render(request, 'tasks/tasks15.html', {'tasks': tasks})



@login_required(login_url='signin')
def create_task15(request):
    print("hello")
    users = User.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        data = request.POST.get('data', '')
        due_date = request.POST['due_date']
        form_attachment = request.FILES.getlist('attachment')
        task = Tasks.objects.create(creator=request.user, data=data, title = title, due_date=due_date)
        task.save()
        print(f'task: {title} is created')
        print(form_attachment)
        for i in form_attachment:
            print(i)
            r= Task_attachment.objects.create(task=task, attachment=i)
        return redirect('control')
    
    return render(request, 'tasks/task_create15.html', {'users': users})



@login_required(login_url='signin')
def show_task(request, pk):
    task = get_object_or_404(Tasks, id=pk)
    reo = Report.objects.filter(task=task)
    for r in reo:
        auth= r.author.all()
        print(auth)
    print(task.assigned.all().count())
    print(task.title)
    # print(reo.author.all())
    return render(request, 'tasks/tasks_view15.html', {"task":task, "report":reo})




"""
    for history
qry = order.history.filter(id=pk)

def historical_changes(qry):

    changes = []

    if qry is not None:

        last = qry.first()

    for all_changes in range(qry.count()):

        new_record, old_record = last, last.prev_record

        if old_record is not None:

            delta = new_record.diff_against(old_record)

            changes.append(delta)

    last = old_record

    return changes

    changes = historical_changes(qry)

    context = { 'changes':changes}
"""

@login_required(login_url='signin')
def accept_task(request, pk):
    print(f"Task ID = {pk}")
    task = get_object_or_404(Tasks, id=pk)
    task.assigned.add(request.user)
    task.status = 1
    task.save()
    print("u are assigned")
    return redirect('tasks')

@login_required(login_url='signin')
def submit_task(req, pk):
    print(f"Task ID = {pk}")
    task = get_object_or_404(Tasks, id=pk)
    task.status = 2
    task.save()
    print('task is handed')
    return redirect('tasks')

@login_required(login_url='signin')
def undo_task(req, pk):
    print(f"Task ID = {pk}")
    task = get_object_or_404(Tasks, id=pk)
    task.status = 1
    task.save()
    print('task is undo')
    return redirect('tasks')