from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.conf import settings
from .models import *
from .serializers import *
from .renderers import *

class StationList(generics.ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    
class StationImage(APIView):
    renderer_classes = [JpegRenderer]
    def get(self, request, station_pk, format=None):
        station_obj = Station.objects.get(pk=station_pk)
        if station_obj.image:
            with open(station_obj.image.path, 'rb') as image_f:
                return Response(image_f.read())
        else:
            with open(os.path.join(settings.MEDIA_ROOT,"no_file_here.jpg"), 'rb') as image_f:
                return Response(image_f.read())

