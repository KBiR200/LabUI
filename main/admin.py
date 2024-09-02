from django.contrib import admin
from .models import Project
from reports.models import report

# Register your models here.
admin.site.register(Project)
admin.site.register(report)