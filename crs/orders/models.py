from django.db import models
from organizations.models import Organization
from clients.models import Client


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='orders')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    amount = models.PositiveIntegerField(verbose_name="Сумма")
    note = models.TextField(verbose_name="Примечание", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.client.name} ({self.client.phone}) - {self.amount}"