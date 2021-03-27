from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from .managers import UserManager


class UserTypeChoices(models.IntegerChoices):
    PARKING_LOT = 0, "PARKING_LOT"
    CUSTOMER = 1, "CUSTOMER"

class VehicleTypeChoices(models.IntegerChoices):
    TWO_WHEELER = 0, "TWO_WHEELER"
    THREE_WHEELER = 1, "THREE_WHEELER"
    FOUR_WHEELER = 2, "FOUR_WHEELER"
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
    ),
    total_parking_slots = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

class Charges(models.Model):
    parkingLotRef = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    vehicle_type = models.IntegerField(
        choices=VehicleTypeChoices.choices,
        default=VehicleTypeChoices.TWO_WHEELER
    )
    charges_per_hour = models.IntegerField(
       validators=[MinValueValidator(0)]  
    )


# class Parking(models.Model):
#     parkingLotRef = models.ForeignKey(ParkingLot, on_delete=models.PROTECT)
#     vehicleRef = models.ForeignKey()