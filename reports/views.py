from django.shortcuts import render
from reports.models import Report
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from chem.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def post(request,pk):
    r= Report.objects.all()
    rep = get_object_or_404(Report, id=pk)
    if request.user.id not in list(rep.author.values_list("id", flat=True)):
        print(list(rep.author.values_list("id", flat=True)))
        print(request.user.id)
        return HttpResponseForbidden("You are not allowed to edit this form.")

    for i in r:
        print(i.author.all().values_list('id',flat=True))
        print(i.author.all().values_list('id',flat=True))
        print(pk)
    return render(request, 'reports.html')