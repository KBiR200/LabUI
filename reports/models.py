from django.db import models
from main.models import Project , Machine
from django.contrib.auth.models import User

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
    
