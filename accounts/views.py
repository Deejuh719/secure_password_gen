from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate, login #new
from django.shortcuts import render, redirect #new
from django.contrib.auth.decorators import login_required #new
from django_otp.plugins.otp_totp.models import TOTPDevice #new

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("password_change_done")
    template_name = "accounts/reset_password.html"

class PasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "registration/password_change_done.html"

class AccountDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "accounts/account_confirm_delete.html"
    model = CustomUser
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        logout(request)
        return super().delete(request, *args, **kwargs)

class AccountSettingsView(LoginRequiredMixin, FormView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("account_settings")
    template_name = "accounts/account_settings.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Account settings updated successfully.")
        return super().form_valid(form)

# new
def login_view(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if user has 2FA enabled
            if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
                # Store user in session for 2FA verification
                request.session["user_id_for_2fa"] = user.id
                return redirect("verify_2fa")
            else:
                # No 2FA, log in directly
                login(request, user)
                return redirect("home")
        else:
            error = "Invalid username or password"

    return render(request, "registration/login.html", {"error": error})

@login_required
def account_settings(request):
    """View for account settings page with 2FA options"""
    has_2fa = TOTPDevice.objects.filter(user=request.user, confirmed=True).exists()

    return render(
        request,
        "accounts/account_settings.html",
        {
            "has_2fa": has_2fa,
        },
    )
