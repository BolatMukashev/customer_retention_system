from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm
from clients.models import Client
from django.db.models import Q


@login_required
def index(request):
    org = request.user.organization

    orders = Order.objects.filter(organization=org)

    return render(request, "orders/index.html", {
        "orders": orders,
        "org": org,
    })


@login_required
def add(request):
    org = request.user.organization

    if request.method == "POST":
        form = OrderForm(request.POST, organization=org)
        if form.is_valid():
            order = form.save(commit=False)
            order.organization = org
            order.save()
            return redirect("orders:index")
    else:
        form = OrderForm(organization=org)

    return render(request, "orders/add.html", {
        "form": form,
        "org": org,
    })

from django.http import JsonResponse


@login_required
def client_search(request):
    org = request.user.organization
    q = request.GET.get('q', '').strip()

    clients = Client.objects.filter(organization=org)
    if q:
        clients = clients.filter(Q(name__icontains=q) | Q(phone__icontains=q))

    clients = clients[:20]

    results = [{"id": c.id, "text": f"{c.name} ({c.phone})"} for c in clients]
    return JsonResponse({"results": results})