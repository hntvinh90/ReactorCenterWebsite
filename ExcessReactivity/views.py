from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import QueryForm
from .models import USING_DATABASE, ER_Years

# To show available files
import os
import json
from django.conf import settings
from django.http import JsonResponse


# Create your views here.
def index(request):
    return query(request)

def send_path(path=[], mother_dir=os.path.join(settings.MEDIA_ROOT, 'excessreactivity')):
    """
    Liet ke cac file va folder trong thu muc <path>
    """

    for root, dirs, files in os.walk(os.path.join(mother_dir, os.sep.join(path))):
        if 'readme.md' in files:
            files.remove('readme.md')
        if dirs or files:
            dirs.sort()
            files.sort()
            return {'dirs': dirs, 'files': files}
    return {'empty': 'True'}


def query(request):
    context = {}
    
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

    # Cac file thong ke co san (nam trong media/operationtiming/) khi truy cap vao index
    if not send_data:
        context.update(send_path())

    context.update({
        'query_form': query_form,
        'send_data': send_data,

        # ON/OFF append_data_from_file
        'data_from_file': False,
    })
    return render(request, 'html/excess_reactivity_page.html', context)

def get_files_and_folders(request):
    if request.method == 'POST':
        path = send_path(request.POST.get('path', '').split('/'))
        print(path)
        return JsonResponse({'path': json.dumps(path)})


@login_required(login_url='/excess_reactivity')
def append_data_from_file(request):
    return index(request)
