from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Password
from .forms import PasswordGeneratorForm, PasswordUpdateForm
from .utils import generate_password
from  django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# TODO: Maybe make this allow you to filter out passwords by app name? date created??
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
    form_class = PasswordGeneratorForm
    template_name = 'passwords/password_create.html'
    success_url = reverse_lazy('password_list')

    def form_valid(self, form):
        generated = generate_password(
            form.cleaned_data['length'],
            form.cleaned_data['include_numbers'],
            form.cleaned_data['include_special'],
            form.cleaned_data['include_similar'],
        )
        
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.app_pass = generated
        self.object.save()

        return super().form_valid(form)

class PasswordUpdateView(LoginRequiredMixin, UpdateView):
    model = Password
    form_class = PasswordUpdateForm
    template_name = 'passwords/password_update.html'
    success_url = reverse_lazy('password_list')

    def form_valid(self, form):
        original_created_at = self.object.created_at
        action = self.request.POST.get('action')
        if action == 'generate':
            generated = generate_password(
                form.cleaned_data['length'],
                form.cleaned_data['include_numbers'],
                form.cleaned_data['include_special'],
                form.cleaned_data['include_similar'],
            )
            form.instance.app_pass = generated

            return self.render_to_response(self.get_context_data(
                form=form,
                generated_password=generated
                ))
        form.instance.created_at = original_created_at
        form.save(update_fields=['app_pass', 'updated_at'])

        return super().form_valid(form)

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)

def generate_password(request):
    if request.method == 'POST':
        form = PasswordGeneratorForm(request.POST)
        if form.is_valid():
            generated = generate_password(
                form.cleaned_data['length'],
                form.cleaned_data['include_numbers'],
                form.cleaned_data['include_special'],
                form.cleaned_data['include_similar'],
            )
            return render(request, 'passwords/password_detail.html', {'generated_password': generated})
    else:
        form = PasswordGeneratorForm()
    return render(request, 'passwords/password_create.html', {'form': form})

class PasswordDeleteView(DeleteView):
    model = Password
    template_name = 'passwords/password_delete.html'
    success_url = reverse_lazy('password_list')

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)
