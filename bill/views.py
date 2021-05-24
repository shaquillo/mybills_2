from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers, models
from platforms.authentication import PlatformsAuthentication

# Create your views here.

class BillViewset(viewsets.ModelViewSet):
    queryset = models.Bill.objects.all()
    serializer_class = serializers.BillSerializer
    permission_classes = [IsAuthenticated,]
    authentication_classes = [PlatformsAuthentication]
