from django.contrib import admin

from libs.alternateDB import AlternateDB
from .models import USING_DATABASE, OperationTime, SaveData
from .forms import AddForm


# Register your models here.
@admin.register(OperationTime)
class OperationTimeAdmin(AlternateDB):
    using = USING_DATABASE
    list_display = ['pk', 'from_power', 'power', 'show_time']
    ''', 'MWd_total', 'time_for_Mwd_up', 'time_for_Mwd_steady',
                    'operation_time_up', 'operation_time_steady', 'MWd_up', 'MWd_steady']  # '''
    form = AddForm

    def show_time(self, obj):
        return '%s - %s, %s' % (
            obj.from_time.strftime("%H:%M"),
            obj.to_time.strftime("%H:%M"),
            obj.date.strftime("%Y/%m/%d")
        )


# @admin.register(SaveData)
class SaveDataAdmin(AlternateDB):
    using = USING_DATABASE
    readonly_fields = ['last_record']
