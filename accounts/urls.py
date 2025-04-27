from django.urls import path
from . import views, two_factor_views
from .views import (SignUpView, PasswordChangeView, 
                    PasswordChangeDoneView, AccountDeleteView, AccountSettingsView)

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('settings/', views.account_settings, name='account_settings'),
    path('2fa/setup/', two_factor_views.setup_2fa, name='setup_2fa'), #new
    path('2fa/disable/', two_factor_views.disable_2fa, name='disable_2fa'), #new
    path('2fa/verify/', two_factor_views.verify_2fa, name='verify_2fa'), #new
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_change/", PasswordChangeView.as_view(), name="reset_password"),
    path("password_change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("account_settings/", AccountSettingsView.as_view(), name="account_settings"),
    path("account_delete/", AccountDeleteView.as_view(), name="account_confirm_delete"),
]