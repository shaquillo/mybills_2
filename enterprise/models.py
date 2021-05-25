from django.db import models
from paymentMethod.models import PaymentMethod

# Create your models here.


class Enterprise(models.Model):
    title = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    image = models.ImageField(upload_to='enterprise', null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    tel = models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    payment_methods = models.ManyToManyField(PaymentMethod)

    class Meta:
        unique_together = ('longitude', 'latitude')
