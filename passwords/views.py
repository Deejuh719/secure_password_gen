from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Password
from .forms import PasswordGeneratorForm, PasswordUpdateForm
from .utils import generate_password
from  django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.db.models.functions import Lower
import json, os
from django.conf import settings
from datetime import datetime

# Create your views here.
class PasswordListView(ListView):
    model = Password
    template_name = 'passwords/password_list.html'
    context_object_name = 'passwords'

    def get_queryset(self):
        # Search the queryset based on the 'search' parameter
        queryset = Password.objects.filter(user=self.request.user)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(app_name__icontains=search_query) |
                Q(app_type__icontains=search_query) |
                Q(username__icontains=search_query) |
                Q(url__icontains=search_query)
                )

        # Sort the queryset based on the 'sort' parameter
        sort_by = self.request.GET.get('sort', 'app_name')
        sort_order = self.request.GET.get('order', 'asc')
        if sort_by in ['app_name', 'app_type', 'created_at', 'updated_at', 'username', 'url']:
            if sort_order == 'desc':
                queryset = queryset.annotate(lower_sort=Lower(sort_by)).order_by(F('lower_sort').desc())
            else:
                queryset = queryset.annotate(lower_sort=Lower(sort_by)).order_by(F('lower_sort').asc())
        else:
            queryset = queryset.annotate(lower_sort=Lower('app_name')).order_by('lower_sort')  # Default sort

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['sort_by'] = self.request.GET.get('sort', 'app_name')
        return context

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
    success_url = reverse_lazy('password_detail')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.app_pass = form.cleaned_data.get('app_pass')
        self.object.save()
        return redirect('password_detail', pk=self.object.pk)
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)

class PasswordRegenerateView(LoginRequiredMixin, UpdateView):
    model = Password
    form_class = PasswordGeneratorForm
    template_name = 'passwords/password_regenerate.html'
    success_url = reverse_lazy('password_detail')

    def form_valid(self, form):
        generated = generate_password(
            form.cleaned_data.get('length', 12),
            form.cleaned_data.get('include_numbers', True),
            form.cleaned_data.get('include_special', True),
            form.cleaned_data.get('include_similar', False),
        )
        self.object = form.save(commit=False)
        self.object.app_pass = generated
        self.object.save(update_fields=['app_pass', 'updated_at'])
        return redirect('password_detail', pk=self.object.pk)
    
    def form_invalid(self, form):
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)

class PasswordDeleteView(DeleteView):
    model = Password
    template_name = 'passwords/password_delete.html'
    success_url = reverse_lazy('password_list')

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)
