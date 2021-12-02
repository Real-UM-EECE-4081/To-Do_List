from django.db import models
from django.contrib.auth.models import User
from django.db.models import F

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    date= models.DateField(blank=True, null=True)
    recurring = models.BooleanField(default=False)
    notes = models.TextField(blank=True,null=True)
    complete = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.name)
    
    class Meta: 
        ordering = [F('date').asc(nulls_last=True)]
    