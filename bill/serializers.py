from rest_framework import serializers
from .models import Bill
from profiles.serializers import SubscriptionSerializer


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['subscription'] =  SubscriptionSerializer(read_only=True)
        return super(BillSerializer, self).to_representation(instance)
