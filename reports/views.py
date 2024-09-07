from django.shortcuts import render
from main.models import Machine
from reports.models import Report, Records
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from chem.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def report(request,pk):
    r= Report.objects.all()
    rep = get_object_or_404(Report, id=pk)
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        return HttpResponseForbidden("You are not allowed to edit this form.")
    return render(request, 'reports.html',{'machines': Machine.objects.all(), 'rep':rep})


def save_record(request, pk):
    if request.method == 'POST':
        try:
            print('ss')
            # Initialize an empty dictionary to hold the JSON data
            form_data = {}

            # Loop through POST data and add the form fields to the dictionary
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken':  # Ignore the CSRF token field
                    form_data[key] = value

            # Print or process the JSON data
            print('Form Data:', form_data)

            # Here you can save the form data to the database if needed
            # For demonstration, just return the data as JSON response
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
    return render(request, 'show_report.html', {'records':related_records})