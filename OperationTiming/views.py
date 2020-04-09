from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .forms import QueryOperationTimingForm, AddOperationTimingForm, DeleteOperationTimingForm
from .models import OperationTime

from datetime import timedelta
from math import log


# Create your views here.
def index(request):
    query_form = QueryOperationTimingForm()
    context = {'query_form': query_form}
    return render(request, 'html/operation_timing_page.html', context)


def query(request):
    for_saving_query = '?%s' % ('&'.join(['='.join([key, request.GET[key]]) for key in request.GET]))
    query_form = QueryOperationTimingForm(request.GET)
    records = OperationTime.objects.all()
    if query_form.is_valid():
        data = query_form.cleaned_data
        if data['fromDate'] >= data['toDate']:
            data['toDate'] = data['fromDate'] + timedelta(1)
        else:
            data['toDate'] += timedelta(1)
        records = records.filter(from_time__gte=data['fromDate'], to_time__lte=data['toDate'])
    else:
        query_form = QueryOperationTimingForm({'fromDate': records.first().from_time.date(), 'toDate': records.last().to_time.date()})
    # Phan tich ket qua nhan duoc de ghi ra bang
    send_data = []
    send_data_total = []
    if records:
        temp = []
        hour = 0
        before = 0
        convert_MWd_to_U235_factor = 1.23
        for record in records:
            if record.power:
                # Truong hop bi dap lo xong len lai thi ghi tiep vao
                if before and temp and before != record.from_time.date():
                    temp[1] = before
                    temp[3] = round(temp[3], 5)
                    temp[4] = round(temp[4], 5)
                    temp[5] = round(temp[4]*convert_MWd_to_U235_factor, 4)
                    temp[7] = round(hour / 60, 1)
                    send_data.append(temp)
                    temp = []
                    before = 0
                if temp:
                    temp[2].append([record.power, round(record.time_for_Mwd)])
                    temp[3] += record.MWd
                    temp[4] = record.MWd_total
                    temp[6] += record.operation_time
                else:
                    temp = [record.from_time.date(),  # from_time
                            record.to_time.date(),    # to_time
                            [[record.power, round(record.time_for_Mwd)]],  # for print power x time (minute)
                            record.MWd, record.MWd_total,
                            0,  # U235 in total from MWd_total
                            record.operation_time,  # operation time in minute each period
                            0   # operation time in hour in total
                            ]
                hour += record.operation_time
            else:
                if temp:
                    before = record.to_time.date()
        if temp not in send_data:
            temp[1] = record.to_time.date()
            temp[3] = round(temp[3], 5)
            temp[4] = round(temp[4], 5)
            temp[5] = round(temp[4]*convert_MWd_to_U235_factor, 4)
            temp[7] = round(hour / 60, 1)
            send_data.append(temp)
    if send_data:
        if query_form.is_valid():
            data = query_form.cleaned_data
            send_data_total = [
                data['fromDate'],
                data['toDate'] - timedelta(1),
                send_data[-1][7],
                send_data[-1][4] - send_data[0][4],
                (send_data[-1][4] - send_data[0][4])*convert_MWd_to_U235_factor
            ]
    context = {
        'query_form': query_form, 'for_saving_query': for_saving_query,
        'send_data': send_data, 'send_data_total': send_data_total
    }
    return render(request, 'html/operation_timing_page.html', context)


@login_required(login_url='/operation_timing')
def add(request):
    if request.method == 'POST':
        error = ''
        form = AddOperationTimingForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['power'] and data['from_time'] > data['to_time']:
                error = 'Thời gian Start không được lớn hơn thời gian Stop.'
            elif OperationTime.objects.filter(to_time__gt=data['from_time']):
                error = 'Khoảng thời gian này đã có trong cơ sở dữ liệu.'
            else:
                try:
                    __calculate_operation_time(form)
                except:
                    error = 'Lỗi khi ghi dữ liệu'
        else:
            error = 'Dữ liệu gửi đi không đúng định dạng.'
        return JsonResponse({'error': error})
    else:
        for_saving_query = '?%s' % ('&'.join(['='.join([key, request.GET[key]]) for key in request.GET]))
        last_records = OperationTime.objects.all().order_by("-from_time")[:5]
        context = {'for_saving_query': for_saving_query,
                   'last_records': last_records}
        return render(request, 'html/add_operation_timing_page.html', context)


def __calculate_operation_time(form):
    new_record = form.save(commit=False)

    # Chi tinh khi cong suat lon hon hoac bang 0.5%/2.5kW
    if new_record.power < 2.5:  # tuong duong 0.5% cua 500kW
        new_record.power = 0

    # Record ngay phia truoc de lay thoi gian, MWd va U235 tong
    # Lay them thong tin cong suat truoc do
    before_record = OperationTime.objects.all().last()
    if before_record:
        if before_record.power:
            # Thoi gian duy tri cong suat cua record truoc do
            t = (new_record.from_time - before_record.to_time).total_seconds() / 60
            before_record.time_for_Mwd += t
            before_record.MWd = before_record.power * before_record.time_for_Mwd / 1440000
            before_record.MWd_total += before_record.MWd
            before_record.operation_time += t
            before_record.save()

            if new_record.power:
                t = (new_record.to_time - new_record.from_time).total_seconds() / 60
                new_record.time_for_Mwd = t * log(2) / abs(log(new_record.power / before_record.power)) / log(2) * abs(
                    1 - before_record.power / new_record.power)
                # Neu cong suat hien tai khac 0 thi cong them thoi gian len cong suat cho viec tinh thoi gian van hanh
                new_record.operation_time = t
            else:
                new_record.time_for_Mwd = 0
                new_record.operation_time = 0
        else:
            # Neu cong suat truoc bang 0
            if new_record.power:
                new_record.time_for_Mwd = 1 / log(2)
            else:
                new_record.time_for_Mwd = 0
            # Thoi gian van hanh se duoc tinh tu luc cong suat dat 0.5%
            new_record.operation_time = 0

        new_record.MWd_total = before_record.MWd_total
    else:
        # Neu la record dau tien
        if new_record.power:
            new_record.time_for_Mwd = 1 / log(2)
        else:
            new_record.time_for_Mwd = 0
        new_record.MWd_total = 0
        new_record.operation_time = 0

    # Cho bang 0 truoc, sau nay nhap record tiep roi tinh
    new_record.MWd = 0

    form.save()


@login_required(login_url='/operation_timing')
def delete(request):
    if request.method == 'POST':
        error = ''
        form = DeleteOperationTimingForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            OperationTime.objects.filter(from_time__gte=date).delete()
        return JsonResponse({'error': error})
    else:
        for_saving_query = '?%s' % ('&'.join(['='.join([key, request.GET[key]]) for key in request.GET]))
        context = {'for_saving_query': for_saving_query}
        return render(request, 'html/delete_operation_timing_page.html', context)


def __recalculate():
    records = OperationTime.objects.all()
    if records:
        for i, record in enumerate(records):
            if record.power:
                if i:
                    if records[i - 1].power:
                        record.time_for_Mwd = (record.to_time - record.from_time).total_seconds() / 60 * log(2) / abs(
                            log(record.power / records[i - 1].power)) / log(2) * abs(
                            1 - records[i - 1].power / record.power)
                    else:
                        record.time_for_Mwd = 1 / log(2)
                else:
                    record.time_for_Mwd = 1 / log(2)
            else:  # cong suat hien tai 0%
                record.time_for_Mwd = 0
            if i and records[i - 1].power:
                records[i - 1].time_for_Mwd += (record.from_time - records[i - 1].to_time).total_seconds() / 60
                records[i - 1].MWd = records[i - 1].power * records[i - 1].time_for_Mwd / 1440000
                records[i - 1].save()
        record.save()
