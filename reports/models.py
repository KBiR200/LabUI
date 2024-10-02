from django.db import models
from main.models import Project , Machine
from django.contrib.auth.models import User
import os
from django.utils.timezone import now
# Create your models here.
class Tasks(models.Model):
    title = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='created_task')
    assigned = models.ManyToManyField(User, default=None, blank=True,
                                       related_name='assigned_task')
    data = models.JSONField(blank=True)
    status = models.IntegerField(name='status', default=0)
    created_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    def __str__(self) -> str:
        return self.title

class Report(models.Model):
    prjct = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)
    title = models.TextField()
    author = models.ManyToManyField(User)
    date_added = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE,
                              related_name='task_report', blank=True, null=True)
    status = models.IntegerField(name='status', default=0)
    def __str__(self) -> str:
        return f"# {self.title}"
    class Meta:
        ordering = ['-date_added']

class Records(models.Model):
    report = models.ManyToManyField(Report, related_name='reports_records')
    data = models.JSONField(blank=True)
    machine = models.ManyToManyField(Machine,related_name='machines',default=1)

    def __str__(self) -> str:
        return f"""record for report {''.join(self.report.values_list('title',
            flat=True))}: {''.join(self.machine.values_list('name',flat=True))} """
    
def custom_upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    new_filename = f"{base}_{now():%Y%m%dT%H%M%S}{extension}"
    print(new_filename)  # Appends timestamp
    return os.path.join("records_attachments/", new_filename)
class Records_attachment(models.Model):
    record = models.ForeignKey(Records,related_name="attachments", on_delete=models.CASCADE)
    attachment= models.FileField(upload_to=custom_upload_to, blank=True, null=True)
    
def task_custom_upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    new_filename = f"{base}_{now():%Y%m%dT%H%M%S}{extension}"
    print(new_filename)  # Appends timestamp
    return os.path.join("task_attachments/", new_filename)
class Task_attachment(models.Model):
    task = models.ForeignKey(Tasks,related_name="attachments", on_delete=models.CASCADE)
    attachment= models.FileField(upload_to=task_custom_upload_to, blank=True, null=True)
    