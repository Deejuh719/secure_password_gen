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
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm 
from django import forms
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required # Added
from qrcode import make as make_qr # Added
from io import BytesIO # Added
import base64 # Added
from django.http import HttpResponse  # Added
import pyotp # Added
from django.contrib.auth import authenticate, login  # Added
from django.shortcuts import render  # Added

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

# new
class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Replace with your user model
        fields = ['email']

class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/account_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_form'] = EmailUpdateForm(instance=self.request.user)
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if 'email' in request.POST:  # Email update form submission
            email_form = EmailUpdateForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, "Your email address has been updated.")
                return redirect('account_settings')
        elif 'old_password' in request.POST:  # Password change form submission
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in
                messages.success(request, "Your password has been updated.")
                return redirect('account_settings')

        # If validation fails, re-render the page with errors
        context = self.get_context_data()
        context['email_form'] = email_form
        context['password_form'] = password_form
        return self.render_to_response(context)

@login_required
def enable_2fa(request):
    user = request.user

    if request.method == "POST":
        # Generate a TOTP secret
        totp = pyotp.TOTP(pyotp.random_base32())
        user.mfa_secret = totp.secret
        user.mfa_enabled = True
        user.save()

        messages.success(request, "Two-Factor Authentication has been enabled.")
        return redirect("account_settings")

    # Generate a QR code for the TOTP secret
    if not user.mfa_secret:
        totp = pyotp.TOTP(pyotp.random_base32())
        user.mfa_secret = totp.secret
        user.save()

    totp = pyotp.TOTP(user.mfa_secret)
    qr_code_data = totp.provisioning_uri(user.email, issuer_name="GimmePasswords")
    qr_code = make_qr(qr_code_data)
    qr_code_io = BytesIO()
    qr_code.save(qr_code_io, format="PNG")
    qr_code_base64 = base64.b64encode(qr_code_io.getvalue()).decode('utf-8')

    return render(request, "accounts/enable_2fa.html", {"qr_code": qr_code_base64})

def login_with_2fa(request):  # Added
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        otp = request.POST.get("otp")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.mfa_enabled:
                totp = pyotp.TOTP(user.mfa_secret)
                if totp.verify(otp):
                    login(request, user)
                    return redirect("home")
                else:
                    messages.error(request, "Invalid OTP.")
            else:
                login(request, user)
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "registration/login.html")
