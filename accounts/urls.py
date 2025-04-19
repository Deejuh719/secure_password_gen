from django.urls import path
from .views import (SignUpView, PasswordChangeView, PasswordChangeDoneView,
                    AccountDeleteView, AccountSettingsView)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("account_settings/", AccountSettingsView.as_view(), name="account_settings"),
    path("account_delete/", AccountDeleteView.as_view(), name="account_confirm_delete"),
]