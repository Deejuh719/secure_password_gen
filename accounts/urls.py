from django.urls import path
from . import views, two_factor_views
from .views import (SignUpView, PasswordChangeView, 
                    PasswordChangeDoneView, AccountDeleteView, AccountSettingsView)

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('settings/', views.account_settings, name='account_settings'),
    path('logout/', views.logout_view, name='logout'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_change/", PasswordChangeView.as_view(), name="reset_password"),
    path("password_change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("account_settings/", AccountSettingsView.as_view(), name="account_settings"),
    path("account_delete/", AccountDeleteView.as_view(), name="account_confirm_delete"),
]