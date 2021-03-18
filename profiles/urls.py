from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'client', views.ClientViewset)
router.register(r'worker', views.WorkerViewset)
router.register(r'subscription', views.SubscriptionViewset)

urlpatterns = [
    path('', include(router.urls))
]