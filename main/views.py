from django.shortcuts import redirect
from django.http import HttpResponse
from django.views import View

class MainRedirect(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('status')
        else:
            return redirect('accounts/login')

# Create your views here.
def status(request):
    return HttpResponse("Hello World")
