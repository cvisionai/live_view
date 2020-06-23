from django.urls import include,path

from . import views
from .views import MainRedirect

urlpatterns = [
    path('', MainRedirect.as_view(), name='home'),
    path('status',views.status,name='status'),
    path('accounts/', include('django.contrib.auth.urls')),
    ]
