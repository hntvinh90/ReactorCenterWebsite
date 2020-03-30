from django import forms

from .models import Event

""" Template
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['fiel_of_Mymodel']
        labels = {'fiel_of_Mymodel': 'label to display'}
        widgets = {'fiel_of_Mymodel': froms.<widget>}
# """

class QueryEventForm(forms.Form):
    fromDate = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}), label='Từ ngày')
    toDate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label='Đến ngày')
    incident = forms.BooleanField(widget=forms.CheckboxInput(), label='Có sự cố', required=False)
    only_me = forms.BooleanField(widget=forms.CheckboxInput(), label='Xem chỉ của tôi', required=False)

class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'description', 'incident']
        labels = {
            'date': 'Ngày',
            'description': 'Các sự kiện',
            'incident': 'Có sự cố'
        }
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': '50'}),
            'incident': forms.CheckboxInput()
        }

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['date', 'description', 'incident']
        labels = {
            'date': 'Ngày',
            'description': 'Các sự kiện',
            'incident': 'Có sự cố'
        }
        widgets = {
            'date': forms.TextInput(attrs={'type': 'date', 'readonly': 'true'}),
            'description': forms.Textarea(attrs={'rows': '50'}),
            'incident': forms.CheckboxInput()
        }
