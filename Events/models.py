from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    date = models.DateField()
    description = models.TextField()
    incident = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
