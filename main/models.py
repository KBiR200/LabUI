from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
class Laberatory(models.Model):
    name = models.CharField(max_length=50,)
    location = models.TextField(null=True)
    LC = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self) -> str:
        return self.name


class Machine(models.Model):
    name = models.CharField(max_length=20)
    form_template = models.TextField(default='add template')
    lab = models.ForeignKey(Laberatory, on_delete=models.CASCADE, related_name='lab_machine',
                             blank=True, null=True)
    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    
    def __str__(self):
        return self.user.username