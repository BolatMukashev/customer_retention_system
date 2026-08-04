# anketa/models.py

from django.db import models
from organizations.models import Organization


class RewardStep(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='reward_steps'
    )
    position = models.PositiveSmallIntegerField(verbose_name='Порядковый номер')
    title = models.CharField(verbose_name='Название награды', max_length=100)

    class Meta:
        ordering = ['position']
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'position'],
                name='unique_reward_position_per_org'
            )
        ]
        verbose_name = 'Шаг анкеты'
        verbose_name_plural = 'Шаги анкеты'

    def __str__(self):
        return f'{self.organization} — {self.position}. {self.title}'