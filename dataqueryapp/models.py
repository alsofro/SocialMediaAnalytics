from django.db import models
from django.conf import settings


class GroupVkProfile(models.Model):
    posts_id = models.IntegerField(verbose_name='id группы vk', default= 0)
    posts_likes = models.PositiveIntegerField(verbose_name='Количество лайков поста', default= 0)
    posts_text = models.TextField(verbose_name='Текст поста группы vk', blank=True)
    posts_date = models.CharField(verbose_name= 'Дата поста ',blank=True, max_length=64 ) 
    posts_comments = models.PositiveIntegerField(verbose_name='Количество комментов поста', default= 0)
    posts_reposts = models.PositiveIntegerField(verbose_name='Количество репостов поста', default= 0)

    def __str__(self):
        return self.post_id