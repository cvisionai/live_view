from django.conf import settings
from django.urls import reverse
from rest_framework import serializers
from .models import *

import os
import logging
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class StationSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    def get_image(self, obj):
        url = reverse('station_image', kwargs={"station_pk": obj.pk})
        return self.context['view'].request.build_absolute_uri(url)
    class Meta:
        model = Station
        fields = ['id', 'name', 'last_updated', 'last_image', 'space_available', 'image']
