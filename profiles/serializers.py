from .models import Client, Worker, Subscription
from rest_framework import serializers
from django.contrib.auth.models import User


class UserClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password']
        write_only_fields = ['password']


class UserWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'is_admin']
        write_only_fields = ['password']


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
        fields = ['id', 'tel', 'user', 'enterprise']

    def to_representation(self, instance):
        self.fields['user'] = UserWorkerSerializer(read_only=True)
        return super(WorkerSerializer, self).to_representation(instance)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
