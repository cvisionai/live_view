from django.conf import settings
from rest_framework import serializers
from .models import *

import os
import logging
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ['id', 'name', 'last_updated', 'space_available']
