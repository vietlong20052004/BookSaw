from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm

class RegisterView(CreateView):
    form_class    = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url   = reverse_lazy('accounts:login')
    success_message = "🎉 Your account was created successfully! Please log in."

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'