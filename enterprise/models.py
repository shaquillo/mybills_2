from django.db import models
from paymentMethod.models import PaymentMethod

# Create your models here.


class Enterprise(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    #image = models.ImageField()
    longitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)
    tel = models.CharField(max_length=9)
    email = models.EmailField()
    payment_methods = models.ManyToManyField(PaymentMethod)

    class Meta:
        unique_together = ('longitude', 'latitude')
