from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Machine(models.Model):
    name = models.CharField(max_length=20)
    form_template = models.TextField(default='add template')
    def __str__(self) -> str:
        return self.name

class Laberatory(models.Model):
    name = models.CharField(max_length=50,)
    location = models.TextField(null=True)
    LC = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self) -> str:
        return self.name


