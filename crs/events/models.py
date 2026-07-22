from datetime import date

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
    created_at = models.DateTimeField(verbose_name='Добавлено', auto_now_add=True)

    MILESTONE_AGES = {18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100}

    class Meta:
        ordering = ['event_date']
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return f'{self.person_name} — {self.get_event_type_display()} ({self.event_date.strftime("%d.%m.%Y")})'

    @property
    def next_occurrence(self):
        """Ближайшая календарная дата этого события — в этом году или в следующем.
        Год хранится в event_date, но для расчёта «скоро ли» он не важен —
        важны только день и месяц."""
        today = date.today()
        try:
            candidate = date(today.year, self.event_date.month, self.event_date.day)
        except ValueError:
            # 29 февраля в невисокосный год — переносим на 1 марта
            candidate = date(today.year, 3, 1)
        if candidate < today:
            try:
                candidate = date(today.year + 1, self.event_date.month, self.event_date.day)
            except ValueError:
                candidate = date(today.year + 1, 3, 1)
        return candidate

    @property
    def days_until(self):
        return (self.next_occurrence - date.today()).days

    @property
    def turning_age(self):
        return self.next_occurrence.year - self.event_date.year

    @property
    def is_milestone(self):
        return self.turning_age in self.MILESTONE_AGES