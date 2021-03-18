from rest_framework import serializers
from .models import Enterprise, EnterprisePaymentMethod


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__'
        depth = 1


class EnterprisePaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnterprisePaymentMethod
        fields = '__all__'
        depth = 1
