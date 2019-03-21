from django.db import models
from django.contrib.auth.models import AbstractUser


class SMAUser(AbstractUser):
    vk_token = models.CharField(max_length=128)
    age = models.PositiveIntegerField(verbose_name = 'возраст', default = 0)
