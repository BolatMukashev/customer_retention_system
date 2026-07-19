from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order


@login_required
def index(request):
    org = request.user.organization

    orders = Order.objects.filter(organization=org)

    return render(request, "orders/index.html", {
        "orders": orders,
        "org": org,
    })