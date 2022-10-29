from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100, verbose_name="Адрес")
    lat = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="Широта")
    lng = models.DecimalField(max_digits=10, decimal_places=6, verbose_name="Долгота")

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.name
