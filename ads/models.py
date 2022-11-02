from django.db import models

from categories.models import Category
from locations.models import Location
from users.models import User


class Ad(models.Model):
    name = models.CharField(max_length=100, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads", verbose_name="Автор")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.CharField(max_length=1000, verbose_name="Описание")
    is_published = models.BooleanField(default=False, verbose_name="Было опубликовано?")
    image = models.ImageField(upload_to="images/", null=True, blank=True, verbose_name="Картинка")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="ads", verbose_name="Категория")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
