from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts")


class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True)
    last_request = models.DateTimeField(
        null=True,
        blank=True,
        default=timezone.now
    )
