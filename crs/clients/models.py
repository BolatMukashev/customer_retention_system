from django.core.validators import RegexValidator
from django.db import models
from organizations.models import Organization
from events.templatetags.event_extras import format_phone
from accounts.models import BaseModel
import uuid


class Client(BaseModel):
    phone_validator = RegexValidator(
        regex=r'^\+?[0-9]{7,15}$',
        message="Введите номер телефона в корректном формате"
    )

    telegram_validator = RegexValidator(
        regex=r'^@?[a-zA-Z]\w{4,31}$',
        message="Введите корректный юзернейм Telegram (5-32 символа: латиница, цифры, подчёркивание, начинается с буквы)"
    )

    id = models.BigAutoField(primary_key=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='clients')
    
    phone = models.CharField(verbose_name="Телефон",
                             max_length=15,
                             validators=[phone_validator])
    
    telegram = models.CharField(verbose_name="Телеграм",
                                max_length=32,
                                blank=True,
                                validators=[telegram_validator])
    
    name = models.CharField(verbose_name="Имя", max_length=100)
    birthday = models.DateField(verbose_name="День рождения", null=True, blank=True)
    note = models.TextField(verbose_name="Примечание", blank=True)
    reward_received = models.BooleanField(verbose_name="Награда получена", default=False)

    anketa_token = models.UUIDField(
        verbose_name="Токен анкеты",
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    anketa_completed_at = models.DateTimeField(verbose_name="Анкета завершена клиентом", null=True, blank=True)
    earned_reward_title = models.CharField(
        verbose_name='Полученная награда',
        max_length=100,
        blank=True,
        help_text='Фиксируется автоматически при завершении анкеты клиентом'
    )
    notified = models.BooleanField(verbose_name="Анкета отправлена", default=False)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(fields=['organization', 'phone'], name='unique_client_phone_per_org')
        ]

    def __str__(self):
        return f"{self.name} ({format_phone(self.phone)})"