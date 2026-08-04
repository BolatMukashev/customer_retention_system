# anketa/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from clients.models import Client
from events.models import Event
from events.forms import AnketaEventForm  # форма создания события остаётся в events — она про Event

from .models import RewardStep


def anketa(request, token):
    client = get_object_or_404(Client, anketa_token=token, is_archived=False)
    reward_steps = list(RewardStep.objects.filter(organization=client.organization))
    total_steps = len(reward_steps)

    if request.method == "POST":
        if request.POST.get("action") == "finish":
            if not client.anketa_completed_at:
                events_count_now = Event.objects.filter(client=client, is_archived=False).count()
                reward_count = min(events_count_now, total_steps)
                earned_title = reward_steps[reward_count - 1].title if reward_count else ''

                client.anketa_completed_at = timezone.now()
                client.earned_reward_title = earned_title
                client.save(update_fields=['anketa_completed_at', 'earned_reward_title'])
            return redirect('anketa:anketa', token=token)

        if not client.anketa_completed_at:
            form = AnketaEventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.client = client
                event.organization = client.organization
                event.save()
                if not client.notified:
                    client.notified = True
                    client.save(update_fields=['notified'])
                return redirect('anketa:anketa', token=token)
    else:
        form = AnketaEventForm()

    events = Event.objects.filter(client=client, is_archived=False).order_by('-created_at')
    events_count = events.count()
    reward_count = min(events_count, total_steps)
    current_reward = reward_steps[reward_count - 1].title if reward_count else None
    progress_percent = int(reward_count / total_steps * 100) if total_steps else 0

    return render(request, "anketa/anketa.html", {
        "client": client,
        "form": form,
        "events": events,
        "events_count": events_count,
        "total_steps": total_steps,
        "reward_steps": reward_steps,
        "is_complete": bool(client.anketa_completed_at),
        "current_reward": client.earned_reward_title if client.anketa_completed_at else current_reward,
        "progress_percent": progress_percent,
        "max_reward_reached": events_count >= total_steps,
        "steps_left": max(0, total_steps - events_count),
    })