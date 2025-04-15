from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Password
from  django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class PasswordListView(ListView):
    model = Password
    template_name = 'passwords/password_list.html'

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)

class PasswordDetailView(DetailView):
    model = Password
    template_name = 'passwords/password_detail.html'

class PasswordCreateView(LoginRequiredMixin, CreateView):
    model = Password
    template_name = 'passwords/password_create.html'
    fields = ['app_name', 'url', 'username', 'app_pass']
    success_url = reverse_lazy('password_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PasswordUpdateView(UpdateView):
    model = Password
    template_name = 'passwords/password_update.html'
    fields = ['app_name', 'url', 'username', 'app_pass']
    success_url = reverse_lazy('password_list')

class PasswordDeleteView(DeleteView):
    model = Password
    template_name = 'passwords/password_delete.html'
    success_url = reverse_lazy('password_list')