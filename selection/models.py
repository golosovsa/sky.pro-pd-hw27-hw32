from django.db import models

from ads.models import Ad
from users.models import User


class Selection(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название подборки")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads", verbose_name="Автор")
    items = models.ManyToManyField(Ad, related_name="selections", verbose_name="Объявления")

    class Meta:
        verbose_name = "Выборка"
        verbose_name_plural = "Выборки"

    def __str__(self):
        return self.name
