from .models import Client, Worker, Subscription
from rest_framework import serializers
from django.contrib.auth.models import User
from enterprise.serializers import EnterpriseSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


class UserClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'tel', 'username', 'password', 'first_name', 'last_name', 'email']


class ClientCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'telCode', 'telVerified', 'telCodeSend']


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = ['id', 'tel', 'username', 'password', 'first_name', 'last_name', 'email', 'enterprise', 'is_admin_w']

    def to_representation(self, instance):
        self.fields['enterprise'] = EnterpriseSerializer(read_only=True)
        return super(WorkerSerializer, self).to_representation(instance)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['enterprise'], self.fields['client'] = EnterpriseSerializer(read_only=True), ClientSerializer(read_only=True)
        return super(SubscriptionSerializer, self).to_representation(instance)


class TOPSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        return data
