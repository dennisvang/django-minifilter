from django.db import models
from django.utils import timezone


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
