import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.urls import reverse

from locations.models import Location


@method_decorator(csrf_exempt, name='dispatch')
class LocationListView(ListView):
    model = Location
    queryset = Location.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        locations = self.object_list
        response = [
            {
                "id": location.id,
                "name": location.name,
                "lat": location.lat,
                "lng": location.lng,
            } for location in locations
        ]

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class LocationDetailView(DetailView):
    model = Location

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        location = self.object

        return JsonResponse({
            "id": location.id,
            "name": location.name,
            "lat": location.lat,
            "lng": location.lng,
        })


@method_decorator(csrf_exempt, name='dispatch')
class LocationUpdateView(UpdateView):
    model = Location
    fields = ["name", "lat", "lng", ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        location_data = json.loads(request.body)

        for field in self.fields:
            if field not in location_data:
                continue
            setattr(self.object, field, location_data[field])

        try:
            self.object.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "lat": self.object.lat,
            "lng": self.object.lng,
        })


@method_decorator(csrf_exempt, name='dispatch')
class LocationCreateView(CreateView):
    model = Location
    fields = ["name", "lat", "lng", ]

    def post(self, request, *args, **kwargs):
        location_data = json.loads(request.body)
        location = Location()
        location.name = location_data.get("name")
        location.lat = location_data.get("lat")
        location.lng = location_data.get("lng")

        try:
            location.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        location.save()
        location_header = reverse("location-detail", kwargs={"pk": location.id})
        return JsonResponse({
            "id": location.id,
            "name": location.name,
            "lat": location.lat,
            "lng": location.lng,
        }, status=201, headers={"Location": location_header})


@method_decorator(csrf_exempt, name='dispatch')
class LocationDeleteView(DeleteView):
    model = Location
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
