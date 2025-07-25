from re import L
from django.shortcuts import render
from laboratory.models import *
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
def lab(request):
    labs = Laberatory.objects.all()
    machines = Machine.objects.all()

    return render(request, 'lab/lab.html', {'labs': labs, 'machines': machines})

def machine(request, pk):
    machine = get_object_or_404(Machine, id=pk)
    return render(request, 'lab/machine.html', {'machine': machine})

def machine_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        lab_id = request.POST.get('lab')
        form_template = request.POST.get('form_template')
        description = request.POST.get('description', '')

        category = get_object_or_404(Machine_Category, id=category_id)
        lab = get_object_or_404(Laberatory, id=lab_id)

        new_machine = Machine(
            name=name,
            form_template=form_template,
            category=category,
            lab=lab,
            description=description,
            machine_responsible=lab.LC,  # Assuming LC is the lab coordinator
        )
        new_machine.save()
        return redirect('lab')

    categories = Machine_Category.objects.all()
    labs = Laberatory.objects.filter(LC = request.user)
    return render(request, 'lab/machine_add.html', {'categories': categories, 'labs': labs})

def machine_edit(request, pk):
    machine = get_object_or_404(Machine, id=pk)
    print(machine.machine_responsible)
    if request.method == 'POST':
        machine.name = request.POST.get('name')
        machine.form_template = request.POST.get('form_template')
        machine.category_id = request.POST.get('category')
        machine.lab_id = request.POST.get('lab')
        machine.description = request.POST.get('description', '')
        machine.serial_number = request.POST.get('serial_number', '…')
        machine.model = request.POST.get('model', '…')
        machine.status = request.POST.get('status')
        
        machine.save()
        return redirect('machine_view', pk=machine.id)

    categories = Machine_Category.objects.all()
    labs = Laberatory.objects.filter(LC=request.user)
    if request.user != machine.machine_responsible:
        return render(request, 'error/error.html', {'message': "You don't have permission to edit this machine."})
    return render(request, 'lab/machine_edit.html', {'machine': machine, 'categories': categories, 'labs': labs})