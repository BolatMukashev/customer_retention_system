from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import Order, StatusType
from .forms import OrderForm
from clients.models import Client
from django.db.models import Q


@login_required
def index(request):
    org = request.user.organization
    
    if org.last_payment_date is None or (timezone.now() - org.last_payment_date) > timedelta(days=365):
        return redirect('pay:index')

    base_qs = Order.objects.filter(organization=org,
                                    is_archived=False,
                                    client__is_archived=False)

    valid_statuses = dict(StatusType.choices)
    status_filter = request.GET.get('status')
    if status_filter not in valid_statuses:
        status_filter = None

    orders = base_qs
    if status_filter:
        orders = orders.filter(status=status_filter)
    orders = orders[:12]

    status_tabs = [
        {"value": value, "label": label, "count": base_qs.filter(status=value).count()}
        for value, label in StatusType.choices
    ]

    return render(request, "orders/index.html", {
        "orders": orders,
        "org": org,
        "status_filter": status_filter,
        "status_tabs": status_tabs,
        "total_count": base_qs.count(),
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
    return render(request, "orders/view.html", {"order": order, "org": org})


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


@require_POST
@login_required
def archive(request, pk):
    org = request.user.organization
    order = get_object_or_404(Order, pk=pk, organization=org)
    order.is_archived = True
    order.archived_at = timezone.now()
    order.save(update_fields=['is_archived', 'archived_at'])
    return redirect('orders:index')


@require_POST
@login_required
def toggle_status(request, pk):
    org = request.user.organization
    order = get_object_or_404(Order, pk=pk, organization=org)

    new_status = request.POST.get('status')
    valid_statuses = dict(StatusType.choices)
    if new_status not in valid_statuses:
        return JsonResponse({"error": "invalid status"}, status=400)

    order.status = new_status
    order.save(update_fields=['status'])
    return JsonResponse({
        "status": order.status,
        "status_display": order.get_status_display(),
    })