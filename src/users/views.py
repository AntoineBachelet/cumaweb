"""File defining the different views used by user application"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreateUserForm

class CreateUserView(LoginRequiredMixin, CreateView):
    """View to create a new User"""
    login_url = "/users/login"
    form_class = CreateUserForm
    model = User
    template_name = "users/createUser.html"
    success_url = reverse_lazy("index")
    
    def form_valid(self, form):
        messages.success(self.request, "Nouvel utilisateur enregistré")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Il y a une erreur dans le formulaire. Merci de vérifier les informations.")
        return super().form_invalid(form)
