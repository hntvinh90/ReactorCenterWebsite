from django.db import models

# Create your models here.
class OperationTime(models.Model):
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    power = models.FloatField()
    time_for_Mwd = models.FloatField()
    MWd = models.FloatField()
    MWd_total = models.FloatField()
    operation_time = models.IntegerField()
