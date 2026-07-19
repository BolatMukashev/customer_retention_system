from django.core.validators import RegexValidator
from django.db import models
from organizations.models import Organization


class Client(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\+?[0-9]{7,15}$',
        message="Введите номер телефона в корректном формате"
    )

    id = models.BigAutoField(primary_key=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='clients')
    phone = models.CharField(verbose_name="Телефон", max_length=15, validators=[phone_validator])
    name = models.CharField(verbose_name="Имя", max_length=100)
    note = models.TextField(verbose_name="Примечание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['organization', 'phone'], name='unique_client_phone_per_org')
        ]

    def __str__(self):
        return f"{self.name} ({self.phone})"