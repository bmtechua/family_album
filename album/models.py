from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    video = models.FileField(upload_to='videos/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Album(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    photos = models.ManyToManyField(
        'Photo', related_name='albums')  # Додаємо related_name
    videos = models.ManyToManyField('Video', related_name='albums')

    def __str__(self):
        return self.name
