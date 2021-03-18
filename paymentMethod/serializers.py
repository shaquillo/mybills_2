from rest_framework import serializers
from .models import PaymentMethod


class PaymentMethodSerializer(serializers.ModelSerializer):
    # enterprises = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')   # enterprises with this payment method

    class Meta:
        model = PaymentMethod
        fields = '__all__'
