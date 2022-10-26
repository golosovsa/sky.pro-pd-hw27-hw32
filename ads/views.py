import json

from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.http import HttpResponseNotAllowed

from .models import Ad, Category


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
        except ValidationError:
            return JsonResponse({"error": "invalid request"}, status=422)

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


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category

    def get(self, *args, **kwargs):
        super().get(*args, *kwargs)
        categories: list[Category] = self.get_queryset()
        response = []
        for category in categories:
            response.append({
                "id": category.pk,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        ad: Category = self.get_object()

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category()
        category.name = category_data.get("name")

        try:
            category.full_clean()
        except ValidationError:
            return JsonResponse({"error": "invalid request"}, status=422)

        category.save()

        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        })
