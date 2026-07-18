from django.db import models
from organizations.models import Organization
from clients.models import Client


class EventType(models.TextChoices):
    BIRTHDAY = 'BIRTHDAY', 'День рождения'
    ANNIVERSARY = 'ANNIVERSARY', 'Годовщина'
    GRADUATION = 'GRADUATION', 'Выпускной'
    HOLIDAY = 'HOLIDAY', 'Праздник'
    EVENT = 'EVENT', 'Мероприятие'


class RelationType(models.TextChoices):
    WIFE = 'WIFE', 'Жена'
    HUSBAND = 'HUSBAND', 'Муж'
    SON = 'SON', 'Сын'
    DAUGHTER = 'DAUGHTER', 'Дочь'
    BOYFRIEND = 'BOYFRIEND', 'Парень'
    GIRLFRIEND = 'GIRLFRIEND', 'Девушка'
    MOTHER = 'MOTHER', 'Мать'
    FATHER = 'FATHER', 'Отец'
    FRIEND = 'FRIEND', 'Друг'
    FEMALE_FRIEND = 'FEMALE_FRIEND', 'Подруга'


class Event(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='events')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='events')
    person_name = models.CharField(verbose_name='Имя', max_length=100)
    relation = models.CharField(verbose_name='Отношение', max_length=50, choices=RelationType.choices)
    event_type = models.CharField(verbose_name='Тип события', max_length=50, choices=EventType.choices)
    event_date = models.DateField(verbose_name='Дата события')

    class Meta:
        ordering = ['event_date']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'{self.person_name} — {self.get_event_type_display()} ({self.event_date})'
