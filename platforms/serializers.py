from .models import Platforms
from rest_framework import serializers


class PlatformsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platforms
        fields = ['name', 'tel', 'email']
        