from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
# from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()

router.register(r'client', views.ClientViewset)
router.register(r'worker', views.WorkerViewset)
router.register(r'subscription', views.SubscriptionViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.TOPViewset.as_view()),
    path('login/refresh/', views.TokenRefreshViewM.as_view()) # Not platform token protected
]