from django.db import models
from django.contrib.auth.models import User


class Passwords(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="passwords")
    app_name = models.CharField(max_length=100)
    password = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user.username}'s password"

    class Meta:
        verbose_name_plural = 'passwords'
