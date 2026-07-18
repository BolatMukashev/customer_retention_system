from django.core.validators import RegexValidator
from django.db import models
from referrals.models import Referral


class TariffType(models.TextChoices):
    BASIC = 'BASIC', 'Базовый'
    PREMIUM = 'PREMIUM', 'Премиум'


class OrganizationType(models.TextChoices):
    FLOWER = 'FLOWER', 'Цветочный магазин'
    CAKE = 'CAKE', 'Кондитерская'
    BALLOONS = 'BALLOONS', 'Магазин шаров'
    ANIMATORS = 'ANIMATORS', 'Аниматоры'
    TOYS = 'TOYS', 'Магазин игрушек'
    RESTAURANT = 'RESTAURANT', 'Ресторан'
    CAFE = 'CAFE', 'Кафе'
    JEWELRY = 'JEWELRY', 'Ювелирный салон'


class Organization(models.Model):
    phone_validator = RegexValidator(
        regex=r'^\+?[0-9]{7,15}$',
        message="Введите номер телефона в корректном формате"
    )

    name = models.CharField(verbose_name="Название", max_length=100, unique=True)
    type = models.CharField(verbose_name="Тип", max_length=20, choices=OrganizationType.choices, default=OrganizationType.FLOWER)
    phone = models.CharField(verbose_name="Телефон", max_length=15, validators=[phone_validator])
    address = models.CharField(verbose_name="Адрес", max_length=200, null=True, blank=True)
    crm_type = models.CharField(verbose_name="CRM", max_length=50, null=True, blank=True)
    kassa_type = models.CharField(verbose_name="Касса", max_length=50, null=True, blank=True)

    referral = models.ForeignKey(to=Referral, verbose_name="Реферал", null=True, blank=True, on_delete=models.SET_NULL, related_name="organizations")

    tariff = models.CharField(verbose_name="Тариф", max_length=20, choices=TariffType.choices, default=TariffType.BASIC)
    is_active = models.BooleanField(verbose_name="Активность", default=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    last_payment_date = models.DateTimeField(verbose_name="Последний платёж", null=True, blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']

    def __str__(self):
        return self.name