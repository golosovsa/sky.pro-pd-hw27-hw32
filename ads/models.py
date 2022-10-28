from django.db import models

from categories.models import Category


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Адрес")
    lat = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="Широта")
    lng = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="Долгота")

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name


class User(models.Model):

    ROLES = (
        ("member", "участник"),
        ("moderator", "модератор"),
        ("admin", "администратор"),
    )

    first_name = models.CharField(max_length=20, verbose_name="Имя")
    last_name = models.CharField(max_length=20, verbose_name="Фамилия")
    username = models.CharField(max_length=20, unique=True, verbose_name="Логин")
    password = models.CharField(max_length=20, verbose_name="Пароль")
    role = models.CharField(max_length=10, choices=ROLES, verbose_name="Роль")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст, полных лет")
    locations = models.ManyToManyField(Location, related_name="users", verbose_name="Локации")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Ad(models.Model):
    name = models.CharField(max_length=100, verbose_name="Заготовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads", verbose_name="Автор")
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.CharField(max_length=1000, verbose_name="Описание")
    is_published = models.BooleanField(default=False, verbose_name="Было опубликовано?")
    image = models.ImageField(upload_to="media/images/", null=True, verbose_name="Картинка")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="ads", verbose_name="Категория")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
