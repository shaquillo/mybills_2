from django.db import models

# Create your models here.


class Platforms(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tel = models.CharField(max_length=20, null=True, default='')
    email = models.EmailField(max_length=100)
    token = models.CharField(max_length=150, unique=True)

    def is_authenticated(self):
        return True
