from django.db import models
from main.models import Project , Machine
from django.contrib.auth.models import User

# Create your models here.
class Report(models.Model):
    prjct = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.TextField()
    author = models.ManyToManyField(User)
    date_added = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"# {self.title}"
    
class Records(models.Model):
    report = models.ManyToManyField(Report)
    data = models.JSONField(blank=True)
    machine = models.ManyToManyField(Machine)

    def __str__(self) -> str:
        return f"record for report: {''.join(self.report.values_list('title',flat=True))} "