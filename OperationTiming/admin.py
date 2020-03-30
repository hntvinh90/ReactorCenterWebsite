from django.contrib import admin

from .models import OperationTime


# Register your models here.
class OperationTimeAdmin(admin.ModelAdmin):
    list_display = ['power', 'time']

    def time(self, obj):
        return '%s - %s, %s' %(obj.from_time.strftime("%H:%M"), obj.to_time.strftime("%H:%M"), obj.from_time.strftime("%m/%d/%Y"))


admin.site.register(OperationTime, OperationTimeAdmin)
