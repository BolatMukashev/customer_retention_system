from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OrganizationSettingsForm


@login_required
def index(request):
    org = request.user.organization

    if request.method == "POST":
        form = OrganizationSettingsForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            return redirect("events:index")
    else:
        form = OrganizationSettingsForm(instance=org)

    return render(request, "settings/index.html", {"form": form, "org": org})