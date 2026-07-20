from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client
from events.models import Event
from orders.models import Order


@login_required
def index(request):
    org = request.user.organization
    clients = Client.objects.filter(organization=org)[:10]
    return render(request, 'clients/index.html', {'clients': clients, "org": org})


@login_required
def view(request, pk):
    org = request.user.organization
    client = get_object_or_404(Client, pk=pk, organization=org)
    events = Event.objects.filter(client=client, organization=org)
    orders = Order.objects.filter(client=client, organization=org)
    return render(request, 'clients/view.html', {'client': client, "events": events, "orders": orders, "org": org})


def add(request):
    pass


def edit(request):
    pass