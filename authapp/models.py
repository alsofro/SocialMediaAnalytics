from django.db import models
from django.contrib.auth.models import AbstractUser

class SMAUser(AbstractUser):
    age = models.PositiveIntegerField(verbose_name = 'возраст', default = 0)

class UserProfile(models.Model):
    user = models.OneToOneField(SMAUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    vk_username = models.CharField(max_length=255, blank=True)
    vk_access_token = models.CharField(max_length=255, blank=True)