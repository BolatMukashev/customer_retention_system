from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client
from .forms import ClientForm
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


@login_required
def add(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.organization = request.user.organization
            client.save()
            return redirect("clients:index")
    else:
        form = ClientForm()

    return render(request, "clients/add.html", {
        "form": form,
    })


@login_required
def edit(request, pk):
    org = request.user.organization
    client = get_object_or_404(Client, pk=pk, organization=org)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("clients:client_view", pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, "clients/edit.html", {
        "form": form,
        "client": client,
    })