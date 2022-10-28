import json

from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed

from ads.models import Ad


@csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
def hello(request):
    return JsonResponse({"status": "ok"})


def choose_method(method_views: dict):
    @csrf_exempt
    def generic_view(request):
        method_view = method_views.get(request.method)
        if not method_view:
            return HttpResponseNotAllowed(list(method_view.keys()))
        return method_view(request)

    return generic_view


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, *args, **kwargs):
        super().get(*args, *kwargs)
        ads: list[Ad] = self.get_queryset()
        response = []
        for ad in ads:
            response.append({
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
            })

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        ad: Ad = self.get_object()

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author", "price", "description", "address", "is_published"]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data.get("name")
        ad.author = ad_data.get("author")
        ad.price = ad_data.get("price")
        ad.description = ad_data.get("description")
        ad.address = ad_data.get("address")
        ad.is_published = ad_data.get("is_published")

        try:
            ad.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.error_dict()}, status=422)

        ad.save()

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published,
        })
