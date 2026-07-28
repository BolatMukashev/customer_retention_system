from django.db import models
from organizations.models import Organization
from clients.models import Client
from accounts.models import BaseModel


class StatusType(models.TextChoices):
    RESERVED = 'RESERVED', 'Резерв'
    PREPAYMENT = 'PREPAYMENT', 'Предоплата'
    PAID = 'PAID', 'Оплочено'


class Order(BaseModel):
    id = models.BigAutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    amount = models.PositiveIntegerField(verbose_name="Сумма")
    note = models.TextField(verbose_name="Примечание", blank=True, null=True)
    status = models.CharField(
            verbose_name="Статус",
            max_length=20,
            choices=StatusType.choices,
            default=StatusType.RESERVED
        )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.client.name} ({self.client.phone}) - {self.amount}"
