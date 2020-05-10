from django.test import TestCase
from django.conf import settings

import datetime

from .models import OperationTime


# Create your tests here.
class OTTestCase(TestCase):
    def setUp(self):
        OperationTime.objects.using('operation_timing').create(
            date=datetime.date(2020, 4, 1),
            from_time=datetime.time(11, 0),
            to_time=datetime.time(11, 30),
            power=0.5 * settings.MAX_POWER / 100
        )