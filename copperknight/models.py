from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False
    )


class Opus(models.Model):
    title = models.CharField(max_length=100,default="Unnamed Opus")
    base64_image = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    img_private = models.BooleanField(default=False)

class FavoritedOpus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opus = models.ForeignKey(Opus, on_delete=models.CASCADE)
