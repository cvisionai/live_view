from django.db import models

class Station(models.Model):
    name = models.CharField(max_length=80)
    last_updated = models.DateTimeField(blank=True,null=True)
    space_available = models.FloatField(blank=True,null=True)
