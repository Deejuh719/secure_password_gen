from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("password_change_done")
    template_name = "registration/password_change_form.html"

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
    
class AccountSettingsView(LoginRequiredMixin, TemplateView):
    model = CustomUser
    success_url = reverse_lazy("account_settings")
    template_name = "accounts/account_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context