# anketa/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from organizations.models import Organization
from .models import RewardStep

DEFAULT_REWARDS = [
    (1, 'Скидка 5%'),
    (2, 'Скидка 10%'),
    (3, 'Скидка 15%'),
    (4, 'Скидка 20%'),
    (5, 'Скидка 25%'),
]


@receiver(post_save, sender=Organization)
def create_default_reward_steps(sender, instance, created, **kwargs):
    if not created:
        return
    RewardStep.objects.bulk_create([
        RewardStep(organization=instance, position=pos, title=title)
        for pos, title in DEFAULT_REWARDS
    ])