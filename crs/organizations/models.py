import re
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from referrals.models import Referral
from django.core.validators import MinValueValidator, MaxValueValidator


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
    GAME_ROOM = 'GAME_ROOM', 'Игровая комната'
    QIZ = 'QIZ', 'Клуб QIZ'


class CurrencyType(models.TextChoices):
    KZT = 'KZT', 'тг'
    RUB = 'RUB', 'руб'
    UZS = 'UZS', 'сум'
    KGS = 'KGS', 'сом'
    USD = 'USD', '$'
    EUR = 'EUR', '€'


class ApplicationStatus(models.TextChoices):
    PENDING = 'PENDING', 'На рассмотрении'
    APPROVED = 'APPROVED', 'Одобрена'
    REJECTED = 'REJECTED', 'Отклонена'


phone_validator = RegexValidator(
    regex=r'^\+?[0-9]{7,15}$',
    message="Введите номер телефона в корректном формате"
)


def normalize_phone(phone):
    """
    Приводит номер к единому виду для хранения и сравнения: только цифры
    с ведущим '+'. Без этого "+77001234567" и "77001234567" считаются
    разными строками и unique/дубль-проверки их не ловят.

    Также учитывает казахстанское/российское правило: ведущая '8' в
    11-значном номере — это то же самое, что '+7' (например, "8747...",
    "+8747..." и "+7747..." — один и тот же номер: после удаления
    нецифровых символов "+8..." и "8..." неотличимы, поэтому оба случая
    покрываются одной проверкой).
    """
    if not phone:
        return phone
    digits = re.sub(r'[^0-9]', '', phone)
    if not digits:
        return phone
    if len(digits) == 11 and digits.startswith('8'):
        digits = '7' + digits[1:]
    return '+' + digits


class Organization(models.Model):
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        verbose_name="Название",
        max_length=100
    )

    type = models.CharField(
        verbose_name="Тип",
        max_length=20,
        choices=OrganizationType.choices,
        default=OrganizationType.FLOWER
    )

    phone = models.CharField(
        verbose_name="Телефон",
        max_length=15,
        unique=True,
        db_index=True,
        validators=[phone_validator]
    )

    address = models.CharField(
        verbose_name="Адрес",
        max_length=200,
        null=True,
        blank=True
    )

    crm_type = models.CharField(
        verbose_name="CRM",
        max_length=50,
        null=True,
        blank=True
    )

    kassa_type = models.CharField(
        verbose_name="Касса",
        max_length=50,
        null=True,
        blank=True
    )

    referral = models.ForeignKey(
        Referral,
        verbose_name="Реферал",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="organizations"
    )

    tariff = models.CharField(
        verbose_name="Тариф",
        max_length=20,
        choices=TariffType.choices,
        default=TariffType.BASIC
    )

    is_active = models.BooleanField(
        verbose_name="Активность",
        default=True
    )

    currency = models.CharField(
        verbose_name="Валюта",
        max_length=10,
        choices=CurrencyType.choices,
        default=CurrencyType.KZT
    )

    upcoming_event_days = models.PositiveSmallIntegerField(
        verbose_name="Показывать события за N дней",
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(30)],
        help_text="За сколько дней до события показывать его на главной странице")

    external_id = models.CharField(
        "ID в CRM",
        max_length=100,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )

    last_payment_date = models.DateTimeField(
        verbose_name="Последний платёж",
        null=True,
        blank=True,
        help_text="Обновляется автоматически из модели Payment (приложение pay)"
    )

    @property
    def subscription_days_left(self):
        if self.last_payment_date is None:
            return None
        end = (self.last_payment_date + timedelta(days=365)).date()
        return (end - timezone.localdate()).days

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ["name"]

    def clean(self):
        super().clean()
        if self.phone:
            self.phone = normalize_phone(self.phone)

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_phone(self.phone)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.phone})"


class Application(models.Model):
    """
    Заявка на подключение — то, что приходит с сайта через форму
    «Зарегистрироваться» / «Подключить». Отдельно от Organization,
    потому что заявку нужно сначала проверить (модерация), прежде
    чем создавать полноценный аккаунт организации.
    """

    id = models.BigAutoField(primary_key=True)

    name = models.CharField(
        verbose_name="Название",
        max_length=100
    )

    type = models.CharField(
        verbose_name="Тип",
        max_length=20,
        choices=OrganizationType.choices,
        default=OrganizationType.FLOWER
    )

    phone = models.CharField(
        verbose_name="Телефон",
        max_length=15,
        db_index=True,
        validators=[phone_validator]
    )

    address = models.CharField(
        verbose_name="Адрес",
        max_length=200,
        null=True,
        blank=True
    )

    tariff = models.CharField(
        verbose_name="Тариф",
        max_length=20,
        choices=TariffType.choices,
        default=TariffType.BASIC
    )

    referral = models.ForeignKey(
        Referral,
        verbose_name="Реферал",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="applications"
    )

    status = models.CharField(
        verbose_name="Статус",
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
        db_index=True
    )

    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
        null=True,
        help_text="Например, причина отказа или заметки при обработке"
    )

    organization = models.OneToOneField(
        Organization,
        verbose_name="Созданная организация",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="application",
        help_text="Заполняется автоматически при одобрении заявки"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создана"
    )

    processed_at = models.DateTimeField(
        verbose_name="Обработана",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Заявка на подключение"
        verbose_name_plural = "Заявки на подключение"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.phone}) — {self.get_status_display()}"

    def clean(self):
        super().clean()
        if self.phone:
            normalized = normalize_phone(self.phone)

            if Organization.objects.filter(phone=normalized).exists():
                raise ValidationError({
                    "phone": "Организация с таким номером телефона уже подключена."
                })

            duplicate_pending = Application.objects.filter(
                phone=normalized,
                status=ApplicationStatus.PENDING,
            ).exclude(pk=self.pk)

            if duplicate_pending.exists():
                raise ValidationError({
                    "phone": "По этому номеру уже есть заявка на рассмотрении."
                })

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_phone(self.phone)
        super().save(*args, **kwargs)

    def approve(self):
        """Создаёт (или переиспользует) Organization на основе заявки и помечает её одобренной."""
        from django.utils import timezone

        if self.status == ApplicationStatus.APPROVED and self.organization_id:
            return self.organization

        normalized = normalize_phone(self.phone)

        # Повторная проверка на случай, если организацию с этим номером
        # успели создать уже после подачи заявки (например, одобрили
        # другую заявку с тем же номером чуть раньше).
        if Organization.objects.filter(phone=normalized).exists():
            raise ValueError(
                f"Организация с номером {normalized} уже существует — заявку нужно отклонить."
            )

        organization = Organization.objects.create(
            name=self.name,
            type=self.type,
            phone=normalized,
            address=self.address,
            tariff=self.tariff,
            referral=self.referral,
            is_active=False,  # включаете вручную после оплаты/настройки
        )

        self.organization = organization
        self.status = ApplicationStatus.APPROVED
        self.processed_at = timezone.now()
        self.save(update_fields=["organization", "status", "processed_at"])
        return organization

    def reject(self, comment=None):
        from django.utils import timezone

        self.status = ApplicationStatus.REJECTED
        self.processed_at = timezone.now()
        if comment:
            self.comment = comment
        self.save(update_fields=["status", "processed_at", "comment"])

