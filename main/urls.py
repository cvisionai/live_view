from django.urls import include,path

from . import views
from .views import MainRedirect
from .rest import *

urlpatterns = [
    path('', MainRedirect.as_view(), name='home'),
    path('status',views.status,name='status'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rest/Stations/', StationList.as_view(), name='station_list'),
    path('rest/StationImage/<int:station_pk>.jpg', StationImage.as_view(), name='station_image'),
    path('rest/StationInfo/<int:station_pk>', StationInfo.as_view(), name='station_info'),
    path('rest/StationInfoByName/<str:station_name>', StationInfoByName.as_view(), name='station_info_by_name')
    ]
