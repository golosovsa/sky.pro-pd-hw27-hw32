from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hello(request):
    return JsonResponse({"status": "ok"})
