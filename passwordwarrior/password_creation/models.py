from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class Passwords(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="passwords")
    app_name = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=250, null=False, blank=False)

    def __str__(self):
        return f"{self.user.username}'s {self.app_name} password"

    class Meta:
        verbose_name_plural = 'passwords'


class Decrypter(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='decrypter')
    decrypt_key = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        validators=[MinLengthValidator(16)],
    )

    def __str__(self):
        return f"{self.user.username}' decrypter"
