from .models import Client, Worker, Subscription
from rest_framework import serializers
from django.contrib.auth.models import User
from enterprise.serializers import EnterpriseSerializer


class UserClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }


class UserWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'tel', 'user'] # 'enterprises'

    def to_representation(self, instance):
        self.fields['user'] = UserClientSerializer(read_only=True)
        return super(ClientSerializer, self).to_representation(instance)


class ClientCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'telCode', 'telVerified', 'telCodeSend']


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = ['id', 'tel', 'user', 'enterprise', 'is_admin']

    def to_representation(self, instance):
        self.fields['user'], self.fields['enterprise'] = UserWorkerSerializer(read_only=True), EnterpriseSerializer(read_only=True)
        return super(WorkerSerializer, self).to_representation(instance)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
