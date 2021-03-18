from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from . import serializers, models

# Create your views here.

class BillViewset(viewsets.ModelViewSet):
    queryset = models.Bill.objects.all()
    serializer_class = serializers.BillSerializer()
