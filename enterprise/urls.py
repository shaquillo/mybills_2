from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'enterprise', views.EnterpriseViewset)
router.register(r'enterprise_payment_method', views.EnterprisePaymentViewset)

urlpatterns = [
    path('', include(router.urls))
]