from django.urls import path
from .views  import (PasswordListView, PasswordDetailView, 
PasswordCreateView, PasswordUpdateView, PasswordDeleteView)

urlpatterns = [
    path("<int:pk>/", PasswordDetailView.as_view(), name="password_detail"),
    path("<int:pk>/update/", PasswordUpdateView.as_view(), name="password_update"),
    path("<int:pk>/delete/", PasswordDeleteView.as_view(), name="password_delete"),
    path("create/", PasswordCreateView.as_view(), name="password_create"),
    path("", PasswordListView.as_view(), name="password_list"),
]
