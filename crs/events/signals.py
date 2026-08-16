# events/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from clients.models import Client
from .models import Event, RelationType, EventType


@receiver(post_save, sender=Client)
def sync_client_birthday_event(sender, instance, **kwargs):
    client = instance
    if client.birthday:
        Event.objects.update_or_create(
            client=client,
            relation=RelationType.SELF,
            event_type=EventType.BIRTHDAY,
            defaults={
                'organization': client.organization,
                'person_name': client.name,
                'event_date': client.birthday,
            },
        )
    else:
        Event.objects.filter(
            client=client,
            relation=RelationType.SELF,
            event_type=EventType.BIRTHDAY,
        ).delete()