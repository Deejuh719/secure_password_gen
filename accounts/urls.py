from django.urls import path
from . import views
from .views import (SignUpView, PasswordChangeView, 
                    PasswordChangeDoneView, AccountDeleteView, AccountSettingsView)

urlpatterns = [
    path('account/', views.AccountSettingsView.as_view(), name='account_settings'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_reset/", PasswordChangeView.as_view(), name="reset_password"),
    path("password_change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("account_settings/", AccountSettingsView.as_view(), name="account_settings"),
    path("account_delete/", AccountDeleteView.as_view(), name="account_confirm_delete"),
    path("account_settings/", AccountSettingsView.as_view(), name="account_settings"),
    path("password_change/", AccountSettingsView.as_view(), name="password_change"),
    path("update_email/", AccountSettingsView.as_view(), name="update_email"),
]