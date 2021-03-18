from django.db import models
from enterprise.models import Enterprise
from profiles.models import Client

# Create your models here.


class Bill(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    creationDate = models.DateTimeField(auto_now_add=True)
    userReceptionDate = models.DateField(auto_now_add=True)
    paymentDateLimit = models.DateField()
    #image = models.ImageField()
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        ordering = ['creationDate']

