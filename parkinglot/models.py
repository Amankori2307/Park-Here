from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .managers import UserManager
from customer.models import VehicleTypeChoices, Vehicle
from django.utils import timezone
class UserTypeChoices(models.IntegerChoices):
    PARKING_LOT = 0, "PARKING_LOT"
    CUSTOMER = 1, "CUSTOMER"

class PaymentMethodChoices(models.IntegerChoices):
    COD = 0, "COD"

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


class ParkingLot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    parking_lot_name = models.CharField(
        max_length=50,
    )
    lat = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )
    long = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )
    total_parking_slots = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

class Charges(models.Model):
    parking_lot_ref = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    vehicle_type = models.IntegerField(
        choices=VehicleTypeChoices.choices,
        default=VehicleTypeChoices.TWO_WHEELER
    )
    charges_per_hour = models.IntegerField(
       validators=[MinValueValidator(0)]  
    )
    class Meta:
        unique_together = ['parking_lot_ref', 'vehicle_type']
    


class Parking(models.Model):
    parking_lot_ref = models.ForeignKey(ParkingLot, on_delete=models.PROTECT)
    vehicle_ref = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    entry_time = models.DateTimeField(
        auto_now=timezone.now
    )
    exit_time = models.DateTimeField(
        null=True
    )
    payment_status = models.BooleanField(
        default=False
    )

class Transaction(models.Model):
    parking_ref = models.ForeignKey(Parking, on_delete=models.PROTECT)
    payment_method = models.IntegerField(
        choices=PaymentMethodChoices.choices,
        default=PaymentMethodChoices.COD
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(0)]
    )