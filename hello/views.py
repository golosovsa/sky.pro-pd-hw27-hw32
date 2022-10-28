from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse


@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def hello(request):
    return JsonResponse({"status": "ok"})
