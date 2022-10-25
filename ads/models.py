from django.db import models


class AdsModel(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=200)
