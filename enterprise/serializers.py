from rest_framework import serializers
from .models import Enterprise
from paymentMethod.serializers import PaymentMethodSerializer


class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = '__all__' # ['id', 'title', 'description', 'longitude', 'latitude','tel', 'email', 'payment_methods', 'workers']

    def to_representation(self, instance):
        self.fields['payment_methods'] = PaymentMethodSerializer(read_only=True, many=True)
        return super(EnterpriseSerializer, self).to_representation(instance)
