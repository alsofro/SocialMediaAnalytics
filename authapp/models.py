from django.db.models.signals import post_save
from django.dispatch import receiver


class SMAUser(AbstractUser):
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

class SMAUserProfile(models.Model):
    user = models.OneToOneField(SMAUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name='имя', max_length=255, blank=True)
    last_name = models.CharField(verbose_name='фамилия', max_length=255, blank=True)
    vk_access_token = models.CharField(verbose_name='ВК токен', max_length=255, blank=True)

    @receiver(post_save, sender=SMAUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            SMAUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=SMAUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.smauserprofile.save()