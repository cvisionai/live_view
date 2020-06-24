from django.db import models
from django.contrib import admin

class Station(models.Model):
    name = models.CharField(max_length=80)
    last_updated = models.DateTimeField(blank=True,null=True, auto_now=True)
    space_available = models.FloatField(blank=True,null=True)
    image = models.FileField(null=True, blank=True)

admin.site.register(Station)
