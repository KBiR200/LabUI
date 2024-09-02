from django.db import models
from main.models import Project
from django.contrib.auth.models import User

# Create your models here.
class report(models.Model):
    prjct = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.TextField()
    formula = models.TextField()
    author = models.ManyToManyField(User)
    date_added = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f"# {self.title}"