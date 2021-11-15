from django.db import models
from django.contrib import admin

import datetime

class Station(models.Model):
    name = models.CharField(max_length=80)
    last_updated = models.DateTimeField(blank=True,null=True)
    last_image = models.DateTimeField(blank=True,null=True)
    space_available = models.FloatField(blank=True,null=True)
    cell_percentage = models.FloatField(blank=True,null=True)
    cell_status = models.CharField(max_length=80, blank=True,null=True)
    image = models.FileField(null=True, blank=True)
    maintenance_required = models.IntegerField(default=0)
    version = models.CharField(max_length=80, blank=True,null=True)
    def __str__(self):
        return f"{self.name} | {self.pk} | {self.maintenance_required} | {self.last_updated} | {self.cell_percentage}"

admin.site.register(Station)
