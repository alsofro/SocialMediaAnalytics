from django.db import models
from django.contrib.auth.models import AbstractUser


class SMAUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name = 'возраст', default = 0)
