from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import BaseRenderer,JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import *
from .models import *
from .serializers import *
from .renderers import *
import datetime
import pytz

from ipware import get_client_ip
import logging
logger = logging.getLogger(__name__)

import datetime
STALE_THRESHOLD = datetime.timedelta(minutes=10)

import io
from twilio.twiml.messaging_response import MessagingResponse

class StationList(generics.ListAPIView):
    queryset = Station.objects.all().order_by('name')
    serializer_class = StationSerializer

class XMLRenderer(BaseRenderer):
    media_type = "text/xml"
    format = "xml"

    def render(self, msg, media_type=None, renderer_context=None):
        """Flattens list of objects into a CSV"""
        return msg

class SMSStatus(APIView):
    queryset = Station.objects.all().order_by('name')
    renderer_classes  =  [XMLRenderer]
    permission_classes = [AllowAny]

    def get(self,  request,  format='xml'):
        stations = Station.objects.all()
        message=""
        for station in stations:
            if station.name.find('-dev') > 0:
                continue
            delta = pytz.utc.localize(datetime.datetime.utcnow())-station.last_updated
            delta_hours =  delta.total_seconds() / 60 / 60
            if delta_hours < 60:
                message += f"{station.name}: Good | "
            else:
                message += f"{station.name}: Last seen {round(delta_hours,2)}  hours ago. | "
        response = MessagingResponse()
        msg = response.message(message)
        return Response(str(response))

class StationInfo(APIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    def get(self, request, station_pk, format=None):
        station_obj = Station.objects.get(pk=station_pk)
        serializer = StationSerializer(station_obj)
        serializer.context['view'] = self
        return Response(serializer.data)

    def post(self, request, station_pk, format=None):
        ip,routable=get_client_ip(request)
        logger.info(f"Station {station_pk} @ {ip}")
        station_obj = Station.objects.get(pk=station_pk)
        station_obj.space_available = request.data.get('space_available',-1.0)
        station_obj.version = request.data.get('version','unknown')
        station_obj.last_updated = timezone.now()
        station_obj.cell_percentage = request.data.get('cell_percentage', None)
        station_obj.cell_status = request.data.get('cell_status', None)
        station_obj.save()
        serializer = StationSerializer(station_obj)
        serializer.context['view'] = self
        return Response(serializer.data)

class StationInfoByName(APIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    def get(self, request, station_name, format=None):
        station_obj = Station.objects.get(name=station_name)
        serializer = StationSerializer(station_obj)
        serializer.context['view'] = self
        return Response(serializer.data)

    def post(self, request, station_name, format=None):
        ip,routable=get_client_ip(request)
        logger.info(f"Station {station_name} @ {ip}")
        station_obj = Station.objects.get(name=station_name)
        station_obj.space_available = request.data.get('space_available',-1)
        station_obj.last_updated = timezone.now()
        station_obj.version = request.data.get('version','unknown')
        station_obj.cell_percentage = request.data.get('cell_percentage', None)
        station_obj.cell_status = request.data.get('cell_status', None)
        station_obj.save()
        serializer = StationSerializer(station_obj)
        serializer.context['view'] = self
        return Response(serializer.data)

class StationImage(APIView):
    renderer_classes = [JpegRenderer]
    def get(self, request, station_pk, format=None):
        station_obj = Station.objects.get(pk=station_pk)


        if station_obj.last_image:
            time_delta = timezone.now() - station_obj.last_image
            if time_delta > STALE_THRESHOLD:
                station_obj.image.delete()

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
        image_name = f"{station_obj.pk}_{station_obj.name}_{timezone.now()}.jpg"
        if station_obj.image:
            station_obj.image.delete()
        station_obj.image.save(image_name, io.BytesIO(request.body))
        station_obj.last_image = timezone.now()
        station_obj.save()
        # Disable image push
        #if settings.TATOR_HOST:
        #    api = tator.get_api(settings.TATOR_HOST, settings.TATOR_TOKEN)
        #    path = os.path.join(settings.MEDIA_ROOT, station_obj.image.name)
        #    tator_image = f"{timezone.now()}.jpg"
        #    for _ in tator.util.upload_media(api, settings.TATOR_TYPE, path=path, section=f"{station_obj.name} LiveView", fname=tator_image):
        #        pass
        self.request.accepted_renderer = JSONRenderer()
        return Response({"message": "Image Updated"})
