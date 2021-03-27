from django.db import models
# from parkinglot.models import User

# Create your models here.


class VehicleTypeChoices(models.IntegerChoices):
    TWO_WHEELER = 0, "TWO_WHEELER"
    THREE_WHEELER = 1, "THREE_WHEELER"
    FOUR_WHEELER = 2, "FOUR_WHEELER"

class Customer(models.Model):
    user = models.OneToOneField('parkinglot.User', on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(
        max_length=50,
        blank=True
    )


class Vehicle(models.Model):
    customer_ref = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle_no = models.CharField(max_length=12)
    vehicle_type = models.IntegerField(
        choices=VehicleTypeChoices.choices,
        default=VehicleTypeChoices.TWO_WHEELER
    )

    class Meta:
        unique_together = ['customer_ref', 'vehicle_no']