from django.contrib import admin
from .models import Project, Machine
from reports.models import Report, Records, Tasks

# Register your models here.
admin.site.register(Project)
admin.site.register(Report)
admin.site.register(Machine)
admin.site.register(Records)
admin.site.register(Tasks)