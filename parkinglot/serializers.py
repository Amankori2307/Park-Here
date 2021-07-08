from datetime import datetime
from rest_framework import serializers
from .models import Parking, ParkingLot, Transaction, User, Charges
from utils.utils import get_avalable_slots
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "mobile") 

class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        exclude = ()


class ChargesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charges
        exclude = ()


class ParkingLotListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)
    charges = serializers.SerializerMethodField("fetch_charges")
    available_slots = serializers.SerializerMethodField("calc_available_slots")
    def calc_available_slots(self, data):
            return get_avalable_slots(data.user.id, data.total_parking_slots)

    def fetch_charges(self, data):
        charges = Charges.objects.filter(parking_lot_ref=data.user.id)
        serializer = ChargesSerializer(charges, many=True)
        return serializer.data
    class Meta:
        model = ParkingLot
        exclude = ()

class ParkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parking
        exclude = ()

class ParkingListSerializer(serializers.ModelSerializer):
    parked_for = serializers.SerializerMethodField("calc_parked_for")
    def calc_parked_for(self, data):
        instance = self.instance
        if instance and instance.exit_time:
            time_diff = instance.exit_time - instance.entry_time
            total_seconds = time_diff.total_seconds()
            total_minutes = int(total_seconds/60)

            hours = total_minutes//60
            minutes = total_minutes%60

            return f"{minutes} minute"
        else:
            return None
    transaction = serializers.SerializerMethodField("fetch_transaction")
    def fetch_transaction(self, data):
        try:
            transaction = Transaction.objects.get(parking_ref=data.id)
            serializer = TransactionSerializer(transaction)
            return serializer.data
        except Transaction.DoesNotExist:
            return False
    parking_lot_ref = ParkingLotListSerializer(read_only=True)
    class Meta:
        model = Parking
        exclude = ()

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ()
