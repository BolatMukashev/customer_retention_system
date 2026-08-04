from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from organizations.models import Organization


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)

    organization = models.ForeignKey(
        Organization,
        verbose_name="Организация",
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(
        verbose_name="Сумма",
        max_digits=10,
        decimal_places=2
    )

    paid_at = models.DateTimeField(
        verbose_name="Дата платежа",
        default=timezone.now
    )

    comment = models.CharField(
        verbose_name="Комментарий",
        max_length=200,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
        ordering = ["-paid_at"]

    def __str__(self):
        return f"{self.organization.name} — {self.amount} ({self.paid_at.date()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._sync_organization_last_payment()

    def _sync_organization_last_payment(self):
        org = self.organization
        if org.last_payment_date is None or self.paid_at > org.last_payment_date:
            org.last_payment_date = self.paid_at
            org.save(update_fields=["last_payment_date"])


@receiver(post_delete, sender=Payment)
def recalc_last_payment_on_delete(sender, instance, **kwargs):
    """
    Если удалили самый свежий платёж — last_payment_date организации
    нужно пересчитать по оставшимся платежам (или обнулить, если их нет).
    """
    org = instance.organization
    latest = org.payments.order_by('-paid_at').first()
    new_date = latest.paid_at if latest else None
    if org.last_payment_date != new_date:
        org.last_payment_date = new_date
        org.save(update_fields=["last_payment_date"])