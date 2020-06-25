from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import *
from .models import *
from .serializers import *
from .renderers import *

import io

class StationList(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer

class StationStatus(APIView):
    pass

class StationImage(APIView):
    renderer_classes = [JpegRenderer]
    def get(self, request, station_pk, format=None):
        station_obj = Station.objects.get(pk=station_pk)
        if station_obj.image:
            with open(station_obj.image.path, 'rb') as image_f:
                return Response(image_f.read())
        else:
            with open(os.path.join(settings.MEDIA_ROOT,"no_data_available.jpg"), 'rb') as image_f:
                return Response(image_f.read())
    def post(self, request, station_pk, format=None):
        print("Content type = " + request.content_type)
        if request.content_type != "image/jpeg":
            raise ValidationError("Required to be an image")
        station_obj = Station.objects.get(pk=station_pk)
        image_name = f"{station_obj.pk}_{station_obj.name}.jpg"
        station_obj.image.save(image_name, io.BytesIO(request.body))
        station_obj.last_image = timezone.now()
        station_obj.save()
        self.request.accepted_renderer = JSONRenderer()
        return Response({"message": "Image Updated"})
