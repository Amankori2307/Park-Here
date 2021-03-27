from rest_framework import serializers
from parkinglot.models import User
from customer.models import Customer
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model: Customer
        fields: '__all__'