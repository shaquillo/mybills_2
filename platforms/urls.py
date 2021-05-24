from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register('', views.PlatformsViewset, basename='platforms-update')

urlpatterns = [
    path('', include(router.urls))
]