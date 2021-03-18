from django.db import models
from paymentMethod.models import PaymentMethod

# Create your models here.


class Enterprise(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    #image = models.ImageField()
    longitude = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=10, null=True, blank=True)
    tel = models.CharField(max_length=9)
    email = models.EmailField()
    payment_methods = models.ManyToManyField(PaymentMethod, through='EnterprisePaymentMethod', through_fields=('enterprise', 'payment_method'))

    class Meta:
        unique_together = ('longitude', 'latitude')


class EnterprisePaymentMethod(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enterprise', 'payment_method')
