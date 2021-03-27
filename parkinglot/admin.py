from django.contrib import admin
from .models import User, ParkingLot, Charges
# Register your models here.
admin.site.register(User)
admin.site.register(ParkingLot)
admin.site.register(Charges)