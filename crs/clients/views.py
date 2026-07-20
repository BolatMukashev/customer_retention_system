from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Client


@login_required
def index(request):
    org = request.user.organization
    clients = Client.objects.filter(organization=org)[:10]
    return render(request, 'clients/index.html', {'clients': clients, "org": org})
