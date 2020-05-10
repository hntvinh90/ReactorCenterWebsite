from django.contrib import admin

from libs.alternateDB import AlternateDB
from .models import USING_DATABASE, ExcessReactivity, ER_Years
from .forms import AddYearForm


# Register your models here.
@admin.register(ER_Years)
class ER_Years_Admin(AlternateDB):
    using = USING_DATABASE
    form = AddYearForm


@admin.register(ExcessReactivity)
class ExcessReactivityAdmin(AlternateDB):
    using = USING_DATABASE
    fieldsets = (
        (None, {
            'fields': (
                'year',
                'date'
            )
        }),
        ('Công suất 0.5% khi chưa có mẫu', {
            'fields': (
                'power05_without_target_4SR',
                'power05_without_target_AR',
                'power05_without_target_ER'
            )
        }),
        ('Công suất 0.5% khi có mẫu', {
            'fields': (
                'power05_4SR',
                'power05_AR',
                'power05_ER'
            )
        }),
        ('Công suất 100% đầu đọt chạy lò', {
            'fields': (
                'power100_start_4SR',
                'power100_start_AR',
                'power100_start_ER'
            )
        }),
        ('Công suất 100% cuối đọt chạy lò', {
            'fields': (
                'power100_end_4SR',
                'power100_end_AR',
                'power100_end_ER'
            )
        }),
    )
