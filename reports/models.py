from django.db import models
from main.models import Project , Machine, Team
from django.contrib.auth.models import User
import os
from django.db.models import Q
from chem import settings
from django.utils.timezone import now
# Create your models here.
class Tasks(models.Model):
    class Urgency(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        CRITICAL = 4, 'Critical'


    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='created_task')
    assigned = models.ManyToManyField(User, default=None, blank=True,
                                       related_name='assigned_task')
    team = models.ForeignKey(Team, on_delete=models.CASCADE,
                             related_name='team_task', blank=True, null=True)
    workers_count = models.IntegerField( default=1)
    data = models.JSONField(blank=True)

    urgency = models.IntegerField(
        choices=Urgency.choices,
        default=Urgency.LOW
    )  # 1: low, 2: medium, 3: high, 4: critical
    status = models.IntegerField(name='status', default=0)
    created_at = models.DateTimeField(default=now)
    start_date = models.DateTimeField(default=now)
    due_date = models.DateTimeField()
    def __str__(self) -> str:
        return self.title

class Report(models.Model):
    prjct = models.ForeignKey(Project, on_delete=models.CASCADE,blank=True, null=True)
    title = models.TextField()
    author = models.ManyToManyField(User)
    date_added = models.DateTimeField(auto_now=now) # type: ignore
    
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE,
                              related_name='task_report', blank=True, null=True)
    status = models.IntegerField(name='status', default=1)
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
    created = models.DateTimeField(auto_now_add=True) 
    task = models.ForeignKey(Tasks,related_name="attachments", on_delete=models.CASCADE)
    attachment= models.FileField(upload_to=task_custom_upload_to, blank=True, null=True)
    class Meta: 
        ordering = ('created',) 

class Task_comment(models.Model): 
    Task = models.ForeignKey(Tasks,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 

    class Meta: 
        ordering = ('created',) 
        
    @classmethod
    def comments_for_user_tasks(cls, user):
        """Return all comments on tasks assigned to the given user."""
        return cls.objects.filter(Q(Task__assigned=user) | Q(Task__creator=user)).exclude(Q(user=user) | ~Q(Task__status=1)).select_related('Task', 'user').distinct()


def machine_custom_upload_to(instance, filename):
    base, extension = os.path.splitext(filename)
    new_filename = f"{base}_{now():%Y%m%dT%H%M%S}{extension}"
    return os.path.join("machine_attachments/", new_filename)

class Machine_attachment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    machine = models.ForeignKey(Machine, related_name="attachments", on_delete=models.CASCADE)
    attachment = models.FileField(upload_to=machine_custom_upload_to, blank=True, null=True)
    
    class Meta: 
        ordering = ('created',)

class Machine_comment(models.Model): 
    machine = models.ForeignKey(Machine,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 

    class Meta: 
        ordering = ('created',) 
        
    def __str__(self):
        return f'Comment by {self.user} on {self.machine}'