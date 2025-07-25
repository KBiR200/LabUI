from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Laberatory(models.Model):
    name = models.CharField(max_length=50,)
    location = models.TextField(null=True)
    LC = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self) -> str:
        return self.name
    
    

class Machine_Category(models.Model):
    slug = models.SlugField(unique=True)        # e.g. "research", "analysis"
    name = models.CharField(max_length=50)      # e.g. "Research", "Analysis"
    
    description = models.TextField(blank=True)  # optional

    def __str__(self):
        return self.name


class Machine(models.Model):
    name          = models.CharField(max_length=50)
    machine_responsible= models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='machine_responsible')
    # machine_responsible = models.ForeignKey(User, on_delete=models.CASCADE, null=True
    form_template = models.TextField(default='…')
    category      = models.ForeignKey(
                        Machine_Category,
                        on_delete=models.PROTECT,
                        default=None,
                        null=True,
                        related_name='machines'
                    )
    lab           = models.ForeignKey(
                        Laberatory,
                        on_delete=models.CASCADE,
                        related_name='lab_machine',
                        blank=True,
                        null=True
                    )
    serial_number = models.TextField(default='…')
    model         = models.TextField(default='…')
    status        = models.BooleanField(default=False) # True if available, False if not available
    description   = models.TextField(blank=True) # optional
    def __str__(self):
        return self.name