from django import forms

from .models import OperationTime

""" Template
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['fiel_of_Mymodel']
        labels = {'fiel_of_Mymodel': 'label to display'}
        widgets = {'fiel_of_Mymodel': froms.<widget>}
# """

class QueryOperationTimingForm(forms.Form):
    fromDate = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'type': 'date'}), label='Từ ngày')
    toDate = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'date'}), label='Đến ngày')

class AddOperationTimingForm(forms.ModelForm):
    class Meta:
        model = OperationTime
        fields = ['from_time', 'to_time', 'power']

class DeleteOperationTimingForm(forms.Form):
    date = forms.DateTimeField()
