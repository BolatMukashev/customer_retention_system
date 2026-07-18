from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from .models import Event


def index(request):
    today = timezone.localdate()
    end_date = today + timedelta(days=3)

    events = Event.objects.filter(event_date__gte=today, event_date__lte=end_date)

    return render(request, 'events/index.html', {'events': events})