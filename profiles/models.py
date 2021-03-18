from django.db import models
from django.contrib.auth.models import User
from enterprise.models import Enterprise

# Create your models here.


class Client(models.Model):
    tel = models.CharField(max_length=9)
    telVerified = models.BooleanField(default=False)
    telCodeSend = models.BooleanField(default=False)
    telCode = models.CharField(max_length=10, default=None, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enterprises = models.ManyToManyField(Enterprise, through='Subscription', through_fields=('client', 'enterprise'))

    #image = models.ImageField()


class Worker(models.Model):
    tel = models.CharField(max_length=9)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #image = models.ImageField()
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)


class Subscription(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('enterprise', 'client')