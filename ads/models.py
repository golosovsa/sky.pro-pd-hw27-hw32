from django.db import models
from django import forms


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.CharField(max_length=1000)
    address = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
