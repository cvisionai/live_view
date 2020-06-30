from django.db import models
from django.contrib import admin

class Station(models.Model):
    name = models.CharField(max_length=80)
    last_updated = models.DateTimeField(blank=True,null=True)
    last_image = models.DateTimeField(blank=True,null=True)
    space_available = models.FloatField(blank=True,null=True)
    image = models.FileField(null=True, blank=True)
    maintenance_required = models.IntegerField(default=0)

admin.site.register(Station)
