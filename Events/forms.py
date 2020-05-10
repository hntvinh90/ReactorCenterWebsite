from django import forms

# from .models import Event


class QueryForm(forms.Form):
    fromDate = forms.DateField(required=True, widget=forms.TextInput(attrs={'type': 'date'}), label='Từ ngày')
    toDate = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label='Đến ngày')
    incident = forms.BooleanField(widget=forms.CheckboxInput(), label='Có sự cố', required=False)
