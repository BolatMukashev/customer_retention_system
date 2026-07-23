from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Client
from .forms import ClientForm
from events.models import Event
from orders.models import Order
from django.db import IntegrityError
import re
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from events.templatetags.event_extras import format_phone
from django.views.decorators.http import require_POST


@login_required
def index(request):
    org = request.user.organization
    clients = Client.objects.filter(organization=org, is_archived=False)[:10]
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
        # Важно: организация должна быть на инстансе ДО is_valid(),
        # иначе Django не сможет проверить уникальность (organization, phone)
        form.instance.organization = request.user.organization
        if form.is_valid():
            try:
                client = form.save(commit=False)
                client.organization = request.user.organization
                client.save()
                return redirect("clients:index")
            except IntegrityError:
                # Подстраховка на случай гонки запросов (race condition)
                form.add_error("phone", "Клиент с таким номером телефона уже существует")
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
            try:
                form.save()
                return redirect("clients:client_view", pk=client.pk)
            except IntegrityError:
                form.add_error("phone", "Клиент с таким номером телефона уже существует")
    else:
        form = ClientForm(instance=client)

    return render(request, "clients/edit.html", {
        "form": form,
        "client": client,
    })


@login_required
def search(request):
    org = request.user.organization
    query = request.GET.get('q', '').strip()
    results = []

    if len(query) >= 2:
        digits = re.sub(r'\D', '', query)
        filters = Q(name__icontains=query) | Q(telegram__icontains=query)
        if digits:
            filters |= Q(phone__icontains=digits)

        clients = Client.objects.filter(organization=org).filter(filters)[:10]
        results = [
            {
                'id': c.pk,
                'text': f"{c.name} — {format_phone(c.phone)}",
                'url': reverse('clients:client_view', args=[c.pk]),
            }
            for c in clients
        ]

    return JsonResponse({'results': results})


@require_POST
@login_required
def archive(request, pk):
    org = request.user.organization
    client = get_object_or_404(Client, pk=pk, organization=org)
    client.is_archived = True
    client.archived_at = timezone.now()
    client.save(update_fields=['is_archived', 'archived_at'])
    return redirect('clients:index')