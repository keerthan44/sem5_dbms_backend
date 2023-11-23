from django.http import HttpResponse, JsonResponse
from auction.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from pickle import FALSE
from django.forms.models import model_to_dict
from authentication.views import authenicate_user

# Create your views here.
@csrf_exempt
def hello(request):
    return HttpResponse("Hello")

def create_auction(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            Auction.objects.create()
        except:
            return JsonResponse({"status": "Invalid Data"}, safe=False, status=400)





