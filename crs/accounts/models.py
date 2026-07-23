
from django.contrib.auth.models import AbstractUser
from django.db import models
from organizations.models import Organization
from .validators import validate_phone
from .managers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    is_archived = models.BooleanField(default=False, verbose_name="Архивирован")
    archived_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата архивации")

    class Meta:
        abstract = True


class User(AbstractUser):
    username = None
    email = None

    phone = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_phone],
    )

    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name="owner",
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Владелец магазина'
        verbose_name_plural = 'Владельцы магазинов'

    def __str__(self):
        return self.phone
    