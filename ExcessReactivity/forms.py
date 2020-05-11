from django import forms

from .models import USING_DATABASE, ER_Years


class AddYearForm(forms.ModelForm):
    model = ER_Years

    def clean(self):
        # Ktra xem nam nhap vao co dung dinh dang khong?
        if self.is_valid():
            year = self.cleaned_data.get('year')
            if not (len(year) == 4 and year.isdigit()):
                self.add_error('year', 'Wrong Format !!!')


class QueryForm(forms.Form):
    # Get tat ca cac nam co trong database
    data = []
    years = ER_Years.objects.using(USING_DATABASE).order_by('-year')
    if years:
        for record in years:
            data.append((record.year, record.year))
    year = forms.ChoiceField(label='Năm', required=True, choices=data)
