from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(primary_key=True, max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    mfa_secret = models.CharField(max_length=16, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.username