from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import QueryForm
from .models import USING_DATABASE, OperationTime, SaveData


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
                query_form.add_error('toDate', 'Sai ngày')
            else:
                # Get data
                records = OperationTime.objects.using(USING_DATABASE).filter(
                    date__gte=data['fromDate'],
                    date__lte=data['toDate']
                )

    # Neu chi GET page
    else:
        query_form = QueryForm()

    # Xu ly data de hien thi len Page
    send_data = []
    if records:
        temp = []  # Luu tam thoi gia tri cho tung dot chay lo
        hour = 0  # Tong thoi gian van hanh
        before = 0  # Kiem tra xem thoi gian lan nay co trung voi lan truoc khong => Fix: bi dap lo xong len lai
        convert_MWd_to_U235_factor = 1.23
        start_query = False  # Fix: Lay du lieu tu dau moi dot chay lo
        for record in records:
            # Bat dau khi from_power == 0
            if not start_query and not record.from_power:
                start_query = True
            if start_query:
                if record.power:

                    # Ngay khac lan truoc => dot chay lo moi => luu du lieu de hien thi
                    if before and temp and before != record.date:
                        temp[1] = before
                        temp[3] = round(temp[3], 5)
                        temp[4] = round(temp[4], 5)
                        temp[5] = round(temp[4] * convert_MWd_to_U235_factor, 4)
                        hour += temp[6]
                        temp[7] = round(hour / 60, 1)
                        send_data.append(temp)
                        temp = []
                        before = 0

                    # Luu tiep gia tri vao temp
                    if temp:
                        temp[2].append([record.power, round(record.time_for_Mwd_up + record.time_for_Mwd_steady)])
                        temp[3] += record.MWd_up + record.MWd_steady
                        temp[4] = record.MWd_total
                        temp[6] += record.operation_time_up + record.operation_time_steady

                    # Neu !temp thi khoi tao cac gia tri theo cau truc sau
                    else:
                        temp = [
                            # 0. fromDate
                            record.date,
                            # 1. toDate
                            record.date,
                            # 2. for print power x time (minute)
                            [[record.power, round(record.time_for_Mwd_up + record.time_for_Mwd_steady)]],
                            # 3. MWd
                            record.MWd_up + record.MWd_steady,
                            # 4. MWd_total
                            record.MWd_total,
                            # 5. U235 in total from MWd_total
                            0,
                            # 6. operation time in minute each period
                            record.operation_time_up + record.operation_time_steady,
                            # 7. operation time in hour in total
                            0
                        ]
                else:
                    if temp:
                        # Luu gia tri ngay dung lo de kiem tra xem co len cong suat lai khong?
                        before = record.date

        # Fix: Chu ki cuoi cung cua vong lap for khong duoc ghi
        if temp:
            # Fix: Chi lay du lieu khi dot chay lo da ket thuc
            if not record.power:
                temp[1] = record.date
                temp[3] = round(temp[3], 5)
                temp[4] = round(temp[4], 5)
                temp[5] = round(temp[4] * convert_MWd_to_U235_factor, 4)
                hour += temp[6]
                temp[7] = round(hour / 60, 1)
                send_data.append(temp)

    # Bang tong ket
    send_data_total = []
    if send_data:
        if query_form.is_valid():
            data = query_form.cleaned_data
            send_data_total = [
                # 0. fromDate
                data['fromDate'],
                # 1. toDate
                data['toDate'],
                # 2. Total operation time
                send_data[-1][7],
                # 3. MWd total of query period
                send_data[-1][4] - send_data[0][4],
                # 4. U235 total of query period
                (send_data[-1][4] - send_data[0][4]) * convert_MWd_to_U235_factor
            ]

    context = {
        'query_form': query_form,
        'send_data': [] if request.GET.get('only_total') else send_data,
        'send_data_total': send_data_total,

        # Thoi gian co trong database
        'first_day': SaveData.get_first_date(),
        'last_day': SaveData.get_last_date(),

        # ON/OFF append_data_from_file
        'data_from_file': False,
    }
    return render(request, 'html/operation_timing_page.html', context)


@login_required(login_url='/operation_timing')
def append_data_from_file(request):
    return index(request)
