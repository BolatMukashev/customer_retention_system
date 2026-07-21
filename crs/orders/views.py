from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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


@login_required
def view(request, pk):
    org = request.user.organization
    order = get_object_or_404(Order, pk=pk, organization=org)
    return render(request, "orders/view.html", {"order": order})


@login_required
def edit(request, pk):
    org = request.user.organization
    order = get_object_or_404(Order, pk=pk, organization=org)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order, organization=org)
        if form.is_valid():
            form.save()
            return redirect("orders:order_view", pk=order.pk)
    else:
        form = OrderForm(instance=order, organization=org)

    return render(request, "orders/edit.html", {"form": form, "order": order})