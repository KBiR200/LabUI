from django.contrib import admin
from .models import Project, Machine, UserProfile, Laberatory
from reports.models import Report, Records, Tasks

# Register your models here.
admin.site.register(Project)
admin.site.register(Laberatory)
admin.site.register(UserProfile)
admin.site.register(Report)
admin.site.register(Machine)
admin.site.register(Records)
admin.site.register(Tasks)