from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Event
from .forms import EventForm


@login_required
def index(request):
    org = request.user.organization
    today = timezone.localdate()
    end_date = today + timedelta(days=3)

    # event_date хранит дату первого события (например, реальный год рождения),
    # поэтому фильтровать «предстоящее» напрямую по event_date нельзя —
    # 1990-07-25 всегда меньше today, сколько бы ни было сегодня.
    # next_occurrence — вычисляемое свойство (день+месяц из event_date,
    # год — текущий или следующий), сравнивать его нужно в Python.
    all_events = Event.objects.filter(organization=org, is_archived=False)
    events = sorted(
        (e for e in all_events if today <= e.next_occurrence <= end_date),
        key=lambda e: e.next_occurrence,
    )

    recent_events = Event.objects.filter(organization=org, is_archived=False).order_by('-created_at')[:6]

    return render(request, 'events/index.html', {
        'events': events,
        'recent_events': recent_events,
        'org': org,
    })


@login_required
def add(request):
    org = request.user.organization

    if request.method == "POST":
        form = EventForm(request.POST, organization=org)
        if form.is_valid():
            event = form.save(commit=False)
            event.organization = org
            event.save()
            return redirect("events:index")
    else:
        form = EventForm(organization=org)

    return render(request, "events/add.html", {"form": form})


@login_required
def view(request, pk):
    org = request.user.organization
    event = get_object_or_404(Event, pk=pk, organization=org)
    return render(request, "events/view.html", {"event": event})


@login_required
def edit(request, pk):
    org = request.user.organization
    event = get_object_or_404(Event, pk=pk, organization=org)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event, organization=org)
        if form.is_valid():
            form.save()
            return redirect("events:event_view", pk=event.pk)
    else:
        form = EventForm(instance=event, organization=org)

    return render(request, "events/edit.html", {"form": form, "event": event})

