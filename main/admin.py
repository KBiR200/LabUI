from django.contrib import admin
from .models import Project, Machine, UserProfile, Laberatory, Team, Machine_Category
from reports.models import Report, Records, Tasks, Records_attachment, Task_comment, Machine_attachment, Machine_comment
from Forms.models import MachineRecordParameter

# Register your models here.
admin.site.register(Project)
admin.site.register(Laberatory)
admin.site.register(UserProfile)
admin.site.register(Report)
admin.site.register(Machine)
admin.site.register(Machine_Category)
admin.site.register(Records)
admin.site.register(Team)
admin.site.register(Tasks)
admin.site.register(Task_comment)
admin.site.register(Records_attachment)
admin.site.register(Machine_attachment)
admin.site.register(Machine_comment)
admin.site.register(MachineRecordParameter)