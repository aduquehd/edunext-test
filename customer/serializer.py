from rest_framework import serializers
from .models import CustomerSetUp


class CustomerSetUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSetUp
        fields = ['id', 'name', 'status', 'data']
