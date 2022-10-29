import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.urls import reverse


from categories.models import Category


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by("name").all()

    def get(self,  request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        categories = self.object_list
        response = [
            {
                "id": category.pk,
                "name": category.name,
            } for category in categories
        ]

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        category = self.object

        return JsonResponse({
            "id": category.pk,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name", ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        try:
            category_data = json.loads(request.body)
        except json.JSONDecodeError as error:
            return JsonResponse({"error": str(error)}, status=422)

        for field in self.fields:
            if field not in category_data:
                continue
            setattr(self.object, field, category_data[field])

        try:
            self.object.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name", ]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        category = Category()
        category.name = category_data.get("name")

        try:
            category.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        category.save()
        location_header = reverse("category-detail", kwargs={"pk": category.id})
        return JsonResponse({
            "id": category.id,
            "name": category.name,
        }, status=201, headers={"Location": location_header})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
