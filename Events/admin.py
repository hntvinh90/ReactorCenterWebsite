from django.contrib import admin
from libs.alternateDB import AlternateDB
from .models import USING_DATABASE, Event


# Register your models here.
@admin.register(Event)
class EventAdmin(AlternateDB):
    using = USING_DATABASE
    list_display = ['from_date_in_str', 'to_date_in_str']

    def from_date_in_str(self, obj):
        return obj.from_date.strftime("%Y/%m/%d")

    def to_date_in_str(self, obj):
        return obj.to_date.strftime("%Y/%m/%d")
