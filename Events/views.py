from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .forms import QueryForm
from .models import USING_DATABASE, Event


# Create your views here.
def index(request):
    return query(request)


def query(request):
    # all data in database
    records = None

    # Neu co yeu cau query data
    if request.GET:
        # Get request form
        query_form = QueryForm(request.GET)

        # Kiem tra query form co hop le khong
        if query_form.is_valid():
            data = query_form.cleaned_data

            # Xu ly khi nguoi dung nhap fromDate > toDate
            if data['fromDate'] > data['toDate']:
                data['toDate'] = data['fromDate']

            records = Event.objects.using(USING_DATABASE).filter(
                Q(from_date__gte=data['fromDate'], from_date__lte=data['toDate'])
                | Q(to_date__gte=data['fromDate'], to_date__lte=data['toDate'])
            ).order_by('from_date')

            # Neu request yeu cau thong tin ve cac su co
            if request.GET.get('incident', ''):
                records = records.filter(incident=True)

    # Neu chi GET page
    else:
        query_form = QueryForm()

    # Tranh tai du lieu qua nhieu => chia du lieu query thanh nhieu page
    number_per_page = 1  # number of date to show in per page
    if records:
        max_page = (len(records) - 1) // number_per_page
    else:
        max_page = 0
    page_number = request.GET.get('page_number')
    # FIX: mot so ngoai le
    if page_number:
        if page_number.isdigit():
            page_number = int(page_number)
            if page_number > max_page:
                page_number = max_page
            if page_number < 0:
                page_number = 0
        else:
            page_number = 0
    else:
        page_number = 0

    context = {
        'events': records[number_per_page * page_number:number_per_page * (page_number + 1)] if max_page else records,
        'query_form': query_form,
        'max_page': max_page,
        'page_number': page_number,

        # Luu lai noi dung request
        'for_saving_query': '&'.join(['='.join([key, value]) for key, value in request.GET.items()]),

        # Thoi gian co trong database
        'first_day': Event.get_first_date(),
        'last_day': Event.get_last_date(),

        # ON/OFF append_data_from_file
        'data_from_file': True,
    }
    return render(request, 'html/events_page.html', context)


@login_required(login_url='/events')
def append_data_from_file(request):
    import os, datetime, shutil
    data_path = os.path.join('media', 'events')
    new_data_path = os.path.join('Events', 'database', 'add')
    date_format = '%Y%m%d'
    for root, _, files in os.walk(new_data_path):
        files.sort()
        for file in files:
            data = file.split('_')
            from_date = datetime.datetime.strptime(data[0], date_format).date()
            to_date = datetime.datetime.strptime(data[1], date_format).date()
            record, created = Event.objects.using(USING_DATABASE).get_or_create(
                from_date=from_date,
                to_date=to_date,
                defaults={
                    'description': file,
                    'incident': True if data[2] == '1' else False
                }
            )
            if not created:
                record.description = '\n'.join([record.description, file])
                record.save()

            # moving file to database
            shutil.move(os.path.join(root, file), os.path.join(data_path, file))
        break
    return index(request)
