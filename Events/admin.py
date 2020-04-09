from django.contrib import admin
from .models import Event


# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['time', 'owner']

    def time(self, obj):
        return obj.date.strftime("%m/%d/%Y")


admin.site.register(Event, EventAdmin)
