# settings/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from anketa.forms import RewardStepFormSet
from anketa.models import RewardStep
from .forms import OrganizationSettingsForm


@login_required
def index(request):
    org = request.user.organization
    reward_qs = RewardStep.objects.filter(organization=org)

    if request.method == "POST" and request.POST.get("form") == "rewards":
        form = OrganizationSettingsForm(instance=org)
        reward_formset = RewardStepFormSet(request.POST, queryset=reward_qs, prefix='rewards')
        if reward_formset.is_valid():
            reward_formset.save(organization=org)
            return redirect("events:index")

    elif request.method == "POST":
        form = OrganizationSettingsForm(request.POST, instance=org)
        reward_formset = RewardStepFormSet(queryset=reward_qs, prefix='rewards')
        if form.is_valid():
            form.save()
            return redirect("events:index")

    else:
        form = OrganizationSettingsForm(instance=org)
        reward_formset = RewardStepFormSet(queryset=reward_qs, prefix='rewards')

    return render(request, "settings/index.html", {
        "form": form,
        "reward_formset": reward_formset,
        "org": org,
    })