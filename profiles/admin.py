from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Client)
admin.site.register(models.Worker)
admin.site.register(models.Subscription)
