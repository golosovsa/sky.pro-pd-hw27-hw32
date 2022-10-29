import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.core.paginator import Paginator
from zavito import settings
from django.db.models import Count, Q

from users.models import User
from locations.models import Location


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(ListView):
    model = User
    queryset = User.objects\
        .prefetch_related("locations")\
        .annotate(total_ads=Count("ads", filter=Q(ads__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        page_number = request.GET.get("page")
        paginator = Paginator(self.object_list, settings.USERS_ON_PAGE)
        users = paginator.get_page(page_number)

        response = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "role": user.role,
                "age": user.age,
                "locations": [location.name for location in user.locations.all()],
                "total_ads": user.total_ads,
            } for user in users
        ]

        return JsonResponse({
            "items": response,
            "total": paginator.count,
            "num_pages": paginator.num_pages,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(DetailView):
    model = User
    queryset = User.objects.prefetch_related("location")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        user = self.object

        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": [location.name for location in user.locations.all()],
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations", ]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        user = User()
        user.first_name = user_data.get("first_name")
        user.last_name = user_data.get("last_name")
        user.username = user_data.get("username")
        user.password = user_data.get("password")
        user.role = user_data.get("role")
        user.age = user_data.get("age")

        try:
            user.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        user.save()

        locations = list(Location.objects.filter(name__in=user_data.get("locations")).all())
        if locations:
            user.locations.add(*locations)
            try:
                user.full_clean()
            except ValidationError:
                pass
            else:
                user.save()

        location_header = reverse("user-detail", kwargs={"pk": user.id})
        return JsonResponse({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": [location.name for location in user.locations.all()],
        }, status=201, headers={"Location": location_header})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations", ]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.first_name = user_data.get("first_name")
        self.object.last_name = user_data.get("last_name")
        self.object.username = user_data.get("username")
        self.object.password = user_data.get("password")
        self.object.role = user_data.get("role")
        self.object.age = user_data.get("age")

        fields = self.fields
        if "locations" in fields:
            fields.remove("locations")

        for field in fields:
            if field not in user_data:
                continue
            setattr(self.object, field, user_data[field])

        if "locations" in user_data:
            locations = list(Location.objects.filter(name__in=user_data.get("locations")).all())
            self.object.locations.clear()
            self.object.locations.add(*locations)

        try:
            self.object.full_clean()
        except ValidationError as error:
            return JsonResponse({"error": error.messages}, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "age": self.object.age,
            "locations": [location.name for location in self.object.locations.all()],
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
