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
from django.contrib.auth.forms import PasswordChangeForm # new
from django import forms # new
from django.shortcuts import redirect # new
from django.contrib.auth import update_session_auth_hash # new

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


