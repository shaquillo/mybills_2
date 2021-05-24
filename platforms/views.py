from django.shortcuts import render
from rest_framework import viewsets, mixins
from .serializers import PlatformsSerializer
from .authentication import PlatformsAuthentication

# Create your views here.

class PlatformsViewset(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    authentication_classes = [PlatformsAuthentication]
    serializer_class = PlatformsSerializer
