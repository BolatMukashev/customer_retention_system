from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from clients.models import Client
from orders.models import Order
from events.models import Event


@login_required
def index(request):
    org = request.user.organization

    context = {
        "clients": Client.objects.filter(organization=org, is_archived=True).order_by('-archived_at'),
        "orders": Order.objects.filter(organization=org, is_archived=True).order_by('-archived_at'),
        "events": Event.objects.filter(organization=org, is_archived=True).order_by('-archived_at'),
    }
    return render(request, "archive/index.html", context)


@login_required
def unarchive_client(request, pk):
    org = request.user.organization
    client = get_object_or_404(Client, pk=pk, organization=org)
    client.is_archived = False
    client.archived_at = None
    client.save(update_fields=['is_archived', 'archived_at'])
    return redirect('archive:index')


@login_required
def unarchive_order(request, pk):
    org = request.user.organization
    order = get_object_or_404(Order, pk=pk, organization=org)
    order.is_archived = False
    order.archived_at = None
    order.save(update_fields=['is_archived', 'archived_at'])
    return redirect('archive:index')


@login_required
def unarchive_event(request, pk):
    org = request.user.organization
    event = get_object_or_404(Event, pk=pk, organization=org)
    event.is_archived = False
    event.archived_at = None
    event.save(update_fields=['is_archived', 'archived_at'])
    return redirect('archive:index')