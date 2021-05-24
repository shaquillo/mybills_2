from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import serializers, models
from rest_framework.permissions import IsAuthenticated
from platforms.authentication import PlatformsAuthentication

# Create your views here.

class EnterpriseViewset(viewsets.ModelViewSet):
    serializer_class = serializers.EnterpriseSerializer
    queryset = models.Enterprise.objects.all()
    permission_classes = [IsAuthenticated,]
    authentication_classes = [PlatformsAuthentication]
