from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import QueryForm
from .models import USING_DATABASE, ER_Years


# Create your views here.
def index(request):
    return query(request)


def query(request):
    send_data = []

    # Neu co yeu cau query data
    if request.GET:
        # Get request form
        query_form = QueryForm(request.GET)

        # Kiem tra query form co hop le khong
        if query_form.is_valid():
            year_record = ER_Years.objects.using(USING_DATABASE).filter(year=query_form.cleaned_data['year'])
            if year_record:
                send_data = year_record[0].excessreactivity_set.all()

    # Neu chi GET page
    else:
        query_form = QueryForm()

    context = {
        'query_form': query_form,
        'send_data': send_data,

        # ON/OFF append_data_from_file
        'data_from_file': False,
    }
    return render(request, 'html/excess_reactivity_page.html', context)


@login_required(login_url='/excess_reactivity')
def append_data_from_file(request):
    return index(request)
