from django.db import models

from datetime import datetime


USING_DATABASE = 'events'


# Create your models here.
class Event(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    description = models.TextField()  # mo ta duong dan toi file anh, cac image cach nhau boi dau xuong dong (enter)

    # Add filters
    incident = models.BooleanField(default=False)
