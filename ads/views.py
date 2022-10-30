import json

from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q


from zavito import settings
from ads.models import Ad


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.select_related("author").order_by("-price")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, *kwargs)
        query = self.object_list

        page_number = request.GET.get("page")
        category_id: str = request.GET.get("cat")
        name_contains_text = request.GET.get("text")
        location_name_contains_text = request.GET.get("location")
        price_from = request.GET.get("price_from")
        price_to = request.GET.get("price_to")

        if category_id and category_id.isdigit():
            query = query.filter(category_id=category_id)

        if name_contains_text:
            query = query.filter(name__icontains=name_contains_text)

        if location_name_contains_text:
            query = query.filter(author__locations__name__icontains=location_name_contains_text)

        if price_from and price_to and price_from.isdigit() and price_to.isdigit():
            query = query.filter(Q(price__gte=price_from) & Q(price__lte=price_to))

        paginator = Paginator(query, settings.ADS_ON_PAGE)
        page = paginator.get_page(page_number)

        response = []
        for ad in page:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author_id": ad.author_id,
                "author": ad.author.first_name,
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published,
                "category_id": ad.category_id,
                "image": ad.image.url if ad.image else None,
            })

        return JsonResponse({
            "items": response,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad
    queryset = Ad.objects.select_related("author")

    def get(self, *args, **kwargs):
        super().get(*args, **kwargs)
        ad: Ad = self.object

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "image": ad.image.url if ad.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ["name", "author_id", "price", "description", "is_published", "category_id", ]

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data.get("name")
        ad.author_id = ad_data.get("author_id")
        ad.price = ad_data.get("price")
        ad.description = ad_data.get("description")
        ad.is_published = ad_data.get("is_published")
        ad.category_id = ad_data.get("category_id")

        try:
            ad.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        ad.save()

        location_header = reverse("ad-detail", kwargs={"pk": ad.id})
        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "price": ad.price,
            "description": ad.description,
            "category_id": ad.category_id,
        }, status=201, headers={"Location": location_header})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "category", ]
    updatable_fields = ["name", "author_id", "price", "description", "category_id", ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        for field in self.updatable_fields:
            if field not in ad_data:
                continue
            setattr(self.object, field, ad_data[field])

        try:
            self.object.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdUploadView(UpdateView):
    model = Ad
    fields = ["image", ]
    success_url = "/"

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES["image"]

        try:
            self.object.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author_id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category_id,
            "image": self.object.image.url if self.object.image else None,
        }, status=201, headers={"Location": self.object.image.url})
