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

    @staticmethod
    def get_first_date():
        try:
            return Event.objects.using(USING_DATABASE).earliest('from_date').from_date
        except:
            return None

    @staticmethod
    def get_last_date():
        try:
            return Event.objects.using(USING_DATABASE).latest('to_date').to_date
        except:
            return None
