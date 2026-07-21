from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import Event


@login_required
def index(request):
    org = request.user.organization
    today = timezone.localdate()
    end_date = today + timedelta(days=3)

    events = Event.objects.filter(event_date__gte=today,
                                  event_date__lte=end_date,
                                  organization=org)

    return render(request, 'events/index.html', {'events': events, "org": org})


def add(request):
    pass


def view(request):
    pass


def edit(request):
    pass

