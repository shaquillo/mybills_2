from django.contrib import admin
from . import models

# Register your models here.
admin.register(models.Client)
admin.register(models.Worker)
admin.register(models.Subscription)
