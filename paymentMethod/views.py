from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import serializers, models
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class PaymentMethodViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PaymentMethodSerializer
    queryset = models.PaymentMethod.objects.all()
    permission_classes = [IsAuthenticated]
