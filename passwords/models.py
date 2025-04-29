from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.hashers import make_password

# Create your models here.

class Password(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='passwords'
    )
    app_name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    username = models.CharField(max_length=255)
    app_pass = models.CharField(max_length=255)
    APP_CATEGORIES = (
        ("Social Media", "Social Media"),
        ("Email", "Email"),
        ("Personal", "Personal"),
        ("Entertainment", "Entertainment"),
        ("Work", "Work"),
        ("Other", "Other"),
    )
    app_type = models.CharField(
        max_length=255,
        choices=APP_CATEGORIES,
        default="Other",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.app_pass = make_password(raw_password)
        self.save()

    def __str__(self):
        return self.app_name

    def get_absolute_url(self):
        return reverse("password_detail", args=[str(self.id)])

    def get_update_url(self):
        return reverse("password_update", args=[str(self.id)])

    def get_delete_url(self):
        return reverse("password_delete", args=[str(self.id)])
