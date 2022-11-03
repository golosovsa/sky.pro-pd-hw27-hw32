from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from locations.models import Location


class User(AbstractUser):
    MEMBER = "member"
    MODERATOR = "moderator"
    ADMIN = "admin"

    ROLES = (
        (MEMBER, "участник"),
        (MODERATOR, "модератор"),
        (ADMIN, "администратор"),
    )

    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=20, verbose_name="Фамилия")
    username = models.CharField(max_length=20, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=256, verbose_name="Пароль")
    role = models.CharField(max_length=10, choices=ROLES, verbose_name="Роль")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст, полных лет", default=0)
    locations = models.ManyToManyField(Location, related_name="users", verbose_name="Локации")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username", ]

    def __str__(self):
        return self.username
