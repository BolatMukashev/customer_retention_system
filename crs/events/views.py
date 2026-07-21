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

    events = Event.objects.filter(event_date__gte=today,
                                  event_date__lte=end_date,
                                  organization=org)

    return render(request, 'events/index.html', {'events': events, "org": org})


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

