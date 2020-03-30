from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Event
from .forms import QueryEventForm, NewEventForm, EditEventForm
from .template import events_template


# Create your views here.
def index(request):
    query_form = QueryEventForm()
    context = {'query_form': query_form,}
    return render(request, 'html/events_page.html', context)


def query_event(request):
    for_saving_query = '?%s' % ('&'.join(['='.join([key, request.GET[key]]) for key in request.GET]))
    user = User.objects.filter(username=request.user.username)
    query_form = QueryEventForm(request.GET)
    events = Event.objects.all().order_by('-date')
    if request.GET.get('incident', ''):
        events = events.filter(incident=True)
    if user and request.GET.get('only_me', ''):
        events = events.filter(owner=request.user)
    if query_form.is_valid():
        data = query_form.cleaned_data
        if data['fromDate'] > data['toDate']:
            data['toDate'] = data['fromDate']
        events = events.filter(date__gte=data['fromDate'], date__lte=data['toDate'])
    else:
        query_form = QueryEventForm({'fromDate': events.last().date, 'toDate': events.first().date})
    number_per_page = 10  # number of date per page
    page_number = int(request.GET.get('page_number', 0))
    max_page = (len(events) - 1) // number_per_page
    if page_number > max_page:
        events = ''
    context = {
        'events': events[number_per_page * page_number:number_per_page * (page_number + 1)] if (events and max_page) else events,
        'query_form': query_form,
        'for_saving_query': for_saving_query,
        'max_page': max_page,
        'page_number': page_number
    }
    return render(request, 'html/events_page.html', context)


@login_required(login_url='/events')
def add_event(request):
    for_saving_query = '?%s' % ('&'.join(['='.join([key, request.GET[key]]) for key in request.GET]))
    error = ''
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = NewEventForm()
    else:
        # POST data submitted; process data.
        form = NewEventForm(request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            check_event = Event.objects.filter(date=new_event.date)
            if check_event:
                error = 'Ngày %s đã có trong cơ sở dữ liệu. Được nhập bởi %s.' % (
                    new_event.date, check_event[0].owner.username)
            else:
                new_event.owner = request.user
                form.save()
                return redirect(
                    reverse('events:query_event') + '?fromDate={0}&toDate={0}&submit='.format(new_event.date))
        else:
            error = 'Dữ liệu gửi đi không đúng định dạng'
    context = {'form': form, 'error': error, 'for_saving_query': for_saving_query, 'events_template': events_template}
    return render(request, 'html/add_event.html', context)


@login_required(login_url='/events')
def del_event(request):
    event_id = request.POST.get('event_id', '')
    if event_id:
        event = Event.objects.get(id=event_id)
        if event.owner == request.user:
            event.delete()
    return JsonResponse({})


@login_required(login_url='/events')
def edit_event(request, event_id):
    for_saving_query = '?%s' % ('&'.join(['='.join([key, request.GET[key]]) for key in request.GET]))
    event = Event.objects.get(id=event_id)
    if event.owner == request.user:
        if request.method != 'POST':
            form = EditEventForm(instance=event)
        else:
            form = EditEventForm(instance=event, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('events:query_event') + '?fromDate={0}&toDate={0}&submit='.format(event.date))
    context = {'form': form, 'event_id': event_id, 'for_saving_query': for_saving_query}
    return render(request, 'html/edit_event.html', context)
