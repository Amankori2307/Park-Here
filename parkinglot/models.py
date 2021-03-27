from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from .managers import UserManager


class UserTypeChoices(models.TextChoices):
    PARKING_LOT = 0, "PARKING_LOT"
    CUSTOMER = 1, "CUSTOMER"
class User(AbstractUser):
    username = None
    email = None
    first_name = None
    last_name = None
    mobile_regex = RegexValidator(regex=r"\d{10}", message="Invalid mobile format(only 10 digit mobile no is allowed)".title())
    mobile = models.CharField(
        max_length=10,
        validators=[mobile_regex],
        unique=True
    )
    user_type = models.IntegerField(
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.CUSTOMER
    )

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.mobile