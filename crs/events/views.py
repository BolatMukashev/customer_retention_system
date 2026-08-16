# events/views.py

from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Avg
from .models import Event, RelationType
from .forms import EventForm
from orders.models import Order


@login_required
def index(request):
    org = request.user.organization
    today = timezone.localdate()

    if org.last_payment_date is None or (timezone.now() - org.last_payment_date) > timedelta(days=365):
        return redirect('pay:index')

    end_date = today + timedelta(days=org.upcoming_event_days)

    proposal_filter = request.GET.get('proposal', '')

    all_events = Event.objects.filter(organization=org,
                                      is_archived=False,
                                      client__is_archived=False)
    if proposal_filter == 'sent':
        all_events = all_events.filter(proposal_sent=True)
    elif proposal_filter == 'not_sent':
        all_events = all_events.filter(proposal_sent=False)

    events = sorted(
        (e for e in all_events if today <= e.next_occurrence <= end_date),
        key=lambda e: e.next_occurrence,
    )

    recent_events = list(Event.objects.filter(organization=org,
                                         is_archived=False,
                                         client__is_archived=False).order_by('-created_at')[:6])

    client_ids = {e.client_id for e in events} | {e.client_id for e in recent_events}
    avg_checks = {
        row['client_id']: row['avg']
        for row in Order.objects.filter(organization=org, client_id__in=client_ids)
                                 .values('client_id')
                                 .annotate(avg=Avg('amount'))
    }
    for e in events:
        e.avg_check = avg_checks.get(e.client_id)
    for e in recent_events:
        e.avg_check = avg_checks.get(e.client_id)

    return render(request, 'events/index.html', {
        'events': events,
        'recent_events': recent_events,
        'org': org,
        'proposal_filter': proposal_filter,
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
    avg_check = Order.objects.filter(client=event.client, organization=org).aggregate(avg=Avg('amount'))['avg']
    return render(request, "events/view.html", {"event": event, "avg_check": avg_check})


@login_required
def edit(request, pk):
    org = request.user.organization
    event = get_object_or_404(Event, pk=pk, organization=org)
    if event.relation == RelationType.SELF:
        return redirect('events:event_view', pk=event.pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event, organization=org)
        if form.is_valid():
            form.save()
            return redirect("events:event_view", pk=event.pk)
    else:
        form = EventForm(instance=event, organization=org)

    return render(request, "events/edit.html", {"form": form, "event": event})


@require_POST
@login_required
def toggle_proposal(request, pk):
    org = request.user.organization
    event = get_object_or_404(Event, pk=pk, organization=org)
    event.proposal_sent = not event.proposal_sent
    event.save(update_fields=['proposal_sent'])
    return JsonResponse({'proposal_sent': event.proposal_sent})


@require_POST
@login_required
def archive(request, pk):
    org = request.user.organization
    event = get_object_or_404(Event, pk=pk, organization=org)
    if event.relation == RelationType.SELF:
        return redirect('events:event_view', pk=event.pk)
    event.is_archived = True
    event.archived_at = timezone.now()
    event.save(update_fields=['is_archived', 'archived_at'])
    return redirect('events:index')
