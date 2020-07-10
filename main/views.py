from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.views import View

from ipware import get_client_ip

import logging
logger = logging.getLogger(__name__)

class MainRedirect(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('status')
        else:
            return redirect('accounts/login')

# Create your views here.
def status(request):
    ip, routable = get_client_ip(request)
    logger.info(f"Status View from {ip}")
    return render(request = request,
                  template_name='status.html')
