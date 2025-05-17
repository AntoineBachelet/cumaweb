"""File defining the different views used by user application"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import CreateUserForm


def is_admin(user):
    """Check if the user is an admin or a superuser"""
    return user.is_staff or user.is_superuser


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to create a new User"""

    login_url = "/users/login/"
    form_class = CreateUserForm
    model = User
    template_name = "users/createUser.html"
    success_url = reverse_lazy("index")

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Nouvel utilisateur enregistré")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Il y a une erreur dans le formulaire. Merci de vérifier les informations.")
        return super().form_invalid(form)


class UserListView(UserPassesTestMixin, ListView):
    """View to list all users"""

    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def test_func(self):
        return is_admin(self.request.user)
