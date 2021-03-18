from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import serializers, models

# Create your views here.

class EnterpriseViewset(viewsets.ModelViewSet):
    serializer_class = serializers.EnterpriseSerializer
    queryset = models.Enterprise.objects.all()


class EnterprisePaymentViewset(viewsets.ModelViewSet):
    serializer_class = serializers.EnterprisePaymentMethodSerializer
    queryset = models.EnterprisePaymentMethod.objects.all()
