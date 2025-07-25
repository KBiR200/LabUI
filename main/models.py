from django.db import models
from django.contrib.auth.models import User
from laboratory.models import Laberatory, Machine, Machine_Category
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
# class Laberatory(models.Model):
#     name = models.CharField(max_length=50,)
#     location = models.TextField(null=True)
#     LC = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     def __str__(self) -> str:
#         return self.name


# class Machine_Category(models.Model):
#     slug = models.SlugField(unique=True)        # e.g. "research", "analysis"
#     name = models.CharField(max_length=50)      # e.g. "Research", "Analysis"
    
#     description = models.TextField(blank=True)  # optional

#     def __str__(self):
#         return self.name


# class Machine(models.Model):
#     name          = models.CharField(max_length=50)
#     form_template = models.TextField(default='…')
#     category      = models.ForeignKey(
#                         Machine_Category,
#                         on_delete=models.PROTECT,
#                         default=None,
#                         null=True,
#                         related_name='machines'
#                     )
#     lab           = models.ForeignKey(
#                         Laberatory,
#                         on_delete=models.CASCADE,
#                         related_name='lab_machine',
#                         blank=True,
#                         null=True
#                     )
#     status        = models.BooleanField(default=False) # True if available, False if not available
#     description   = models.TextField(blank=True) # optional
#     def __str__(self):
#         return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervisor_team', blank=True, null=True)
    members = models.ManyToManyField(User, related_name='team_members', blank=True)
    machine = models.ManyToManyField(Machine, related_name='machine_team', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_team', blank=True, null=True)
    lab = models.ForeignKey(Laberatory, on_delete=models.CASCADE, related_name='lab_team', blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_supervisor = models.BooleanField(default=False)
    supervisor = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='employees')

    
    def __str__(self):
        return self.user.username
    
    def get_supervisor_users(self):
        # Return a QuerySet of all User objects who are the supervisors
        return User.objects.filter(userprofile__in=self.supervisor.all())