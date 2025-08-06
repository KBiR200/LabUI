from django.db import models
from django.contrib.auth.models import User
from laboratory.models import Laberatory, Machine, Machine_Category
# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

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
    department = models.CharField(max_length=100, blank=True, null=True)
    supervisor = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='employees')
    position = {
        'technician': 'Technician',
        'scientist': 'Scientist',
        'laboratory_manager': 'Laboratory Manager',
        'manager': 'Manager',
    }
    
    role = models.CharField(max_length=50, choices=[(key, value) for key, value in position.items()], default='technician')
    
    def __str__(self):
        return self.user.username
    
    def get_team_members(self):
        # Return a QuerySet of all User objects who are members of teams supervised by this user
        return Team.objects.filter(members=self.user).distinct()
    
    def get_teams(self):
        # Return a QuerySet of all Team objects supervised by this user
        return " , ".join(map(str, (list(Team.objects.filter(members=self.user).values_list('name', flat=True)))))
    
    def get_supervisor_users(self):
        # Return a QuerySet of all User objects who are the supervisors
        return User.objects.filter(userprofile__in=self.supervisor.all())