from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Password

class PasswordTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(username="testuser", password="testpassword")

        # Create a test password entry
        self.password = Password.objects.create(
            user=self.user,
            app_name="Test App",
            url="https://testapp.com",
            username="testuser",
            app_pass="testpassword123",
            app_type="Personal",
        )

    def test_password_creation(self):
        response = self.client.post(reverse("password_create"), {
            "app_name": "New App",
            "url": "https://newapp.com",
            "username": "newuser",
            "app_pass": "newpassword123",
            "app_type": "Personal",
            "length": 12,
            "include_numbers": True,
            "include_special": True,
            "include_similar": True,
        }
    )
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Password.objects.filter(app_name="New App").exists())

    def test_password_update(self):
        response = self.client.post(reverse("password_update", args=[self.password.pk]), {
            "app_name": "Test App",  # App name is disabled in the form
            "url": "https://updatedapp.com",
            "username": "updateduser",
            "app_pass": "updatedpassword123",
            "app_type": "Personal",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.password.refresh_from_db()
        self.assertEqual(self.password.url, "https://updatedapp.com")
        self.assertEqual(self.password.username, "updateduser")
        self.assertEqual(self.password.app_pass, "updatedpassword123")
        self.assertEqual(self.password.app_type, "Personal")

    def test_password_deletion(self):
        response = self.client.post(reverse("password_delete", args=[self.password.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Password.objects.filter(pk=self.password.pk).exists())

    def test_password_list_view(self):
        response = self.client.get(reverse("password_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test App")

    def test_password_detail_view(self):
        response = self.client.get(reverse("password_detail", args=[self.password.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test App")
        self.assertContains(response, "https://testapp.com")
        self.assertContains(response, "testuser")

    def test_password_regeneration(self):
        response = self.client.post(reverse("password_regenerate", args=[self.password.pk]), {
            "length": 12,
            "include_numbers": True,
            "include_special": True,
            "include_similar": False,
            "app_type": "Personal",
            "app_name": "Test App",
            "url": "https://testapp.com",
            "username": "testuser",
        })
        self.assertEqual(response.status_code, 302)  # Redirect after regeneration
        self.password.refresh_from_db()
        self.assertNotEqual(self.password.app_pass, "testpassword123")  # Password should be updated