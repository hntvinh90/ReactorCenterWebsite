from django import forms
from django.conf import settings

from datetime import datetime, date

from .models import OperationTime, SaveData


class QueryForm(forms.Form):
    fromDate = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}), label='Từ ngày')
    toDate = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}), label='Đến ngày')
    only_total = forms.BooleanField(label='Chỉ lấy kết quả thống kê', required=False)


class AddForm(forms.ModelForm):
    class Meta:
        model = OperationTime
        fields = ['date', 'from_time', 'to_time', 'power']
        labels = {
            'from_time': 'Start Time:',
            'to_time': 'Stop Time:',
            'power': 'Power (%% of %skW):' % settings.MAX_POWER
        }

    def clean(self):
        data = self.cleaned_data
        from_time = data.get('from_time')
        to_time = data.get('to_time')
        power = data.get('power')

        if from_time:
            if to_time:
                # from_time khong duoc lon hon to_time
                if from_time > to_time:
                    self.add_error('from_time', 'Start Time can not be greater than Stop Time')
            else:
                # Neu to_time khong nhap vao thi bang from_time
                data['to_time'] = data['from_time']

        if power:
            # power phai lon hon 0
            if power < 0:
                self.add_error('power', 'Power must be greater than 0.')
            else:
                # Neu power < MIN_POWER thi xem nhu bang 0
                if power < settings.MIN_POWER:
                    data['power'] = 0
                else:
                    data['power'] *= settings.MAX_POWER / 100

        if self.is_valid():

            # Kiem tra thoi gian nhap vao da co trong database chua?
            last_record = SaveData.get_last_record()
            if last_record:
                if datetime.combine(last_record.date, last_record.to_time) > datetime.combine(data['date'], from_time):
                    raise forms.ValidationError('This period is available in database.')

            # Neu power == 0 thi to_time = from_time
            if not power:
                data['to_time'] = data['from_time']

            # self.add_error('power', 'For testing.')

        return data

    def __init__(self, *args, **kwargs):
        super(AddForm, self).__init__(*args, **kwargs)

        # Gia tri khoi tao cua truong date khi add them record moi
        # Gia tri nay la gia tri cua last record hoac la cua today
        last_record = SaveData.get_last_record()
        self.fields['date'].initial = last_record.date if last_record else date.today()

        # Them placeholder cho cac input
        self.fields['date'].widget.attrs.update({'placeholder': 'yyyy-mm-dd'})
        self.fields['from_time'].widget.attrs.update({'autofocus': 'autofocus', 'placeholder': 'hh:mm'})
        self.fields['to_time'].widget.attrs.update({'placeholder': 'hh:mm'})
        self.fields['power'].widget.attrs.update({'placeholder': '>= 0%'})
