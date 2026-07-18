from django.db import models
from django.core.validators import MaxValueValidator
from accounts.validators import validate_phone


class Referral(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=100)

    phone = models.CharField(
        verbose_name="Телефон",
        max_length=20,
        unique=True,
        validators=[validate_phone]
    )

    commission_percent = models.PositiveSmallIntegerField(
        verbose_name="Комиссия (%)",
        default=50,
        validators=[MaxValueValidator(100)],
    )

    is_active = models.BooleanField(
        verbose_name="Активность",
        default=True,
    )

    class Meta:
        verbose_name = "Реферал"
        verbose_name_plural = "Рефералы"

    def __str__(self):
        return self.first_name