
from django.contrib.auth.models import AbstractUser
from django.db import models
from organizations.models import Organization
from .validators import validate_phone
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = None

    phone = models.CharField(
    max_length=20,
    unique=True,
    validators=[validate_phone],
)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='users',
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
    