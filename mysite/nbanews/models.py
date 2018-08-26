from django.db import models

# Create your models here.
class News(models.Model):
    title = models.TextField(max_length=50, blank=True, null=True, default='')
    author = models.TextField(max_length=100, blank=True, null=True, default='')
    link = models.TextField(max_length=100, blank=True, null=True, default='')
    body = models.TextField(blank=True, null=True, default='')
    small_image = models.TextField(max_length=500, blank=True, null=True, default='')
    image_link = models.TextField(max_length=500, blank=True, null=True, default='')
    video = models.TextField(max_length=500, blank=True, null=True, default='')