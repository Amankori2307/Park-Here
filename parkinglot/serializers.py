from rest_framework import serializers
from .models import ParkingLot, User, Charges


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "mobile") 

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        exclude = ()

class ParkingLotListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    class Meta:
        model = ParkingLot
        exclude = ()

class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        exclude = ()

