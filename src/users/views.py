"""File defining the different views used by user application"""

from django import forms
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from catalog.models import AgriculturalTool, BorrowTool

from .forms import CreateUserForm


def is_admin(user):
    """Check if the user is an admin or a superuser"""
    return user.is_staff or user.is_superuser


class CustomUserChangeForm(UserChangeForm):
    """Form to edit user without password change"""

    class Meta:
        """Main form class"""

        model = User
        fields = ["username", "first_name", "last_name", "email", "is_staff", "is_superuser"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_superuser": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        help_texts = {
            "username": "Requis. 150 caractères maximum. Uniquement des lettres, chiffres et @/./+/-/_.",
            "is_staff": "Permet à l'utilisateur d'accéder à l'interface d'administration.",
            "is_superuser": "Donne tous les droits à l'utilisateur sans avoir à les attribuer explicitement.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            self.fields.pop("password")


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


class UserEditView(UserPassesTestMixin, UpdateView):
    """View to edit user"""

    model = User
    form_class = CustomUserChangeForm
    template_name = "users/createUser.html"
    success_url = reverse_lazy("users:listUser")

    def test_func(self):
        return is_admin(self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "L'utilisateur a été modifié avec succès.")
        return super().form_valid(form)


class UserDeleteView(UserPassesTestMixin, DeleteView):
    """View to delete user"""

    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:listUser")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_to_delete = self.get_object()

        # Vérifier les dépendances
        tools_responsible = AgriculturalTool.objects.filter(user=user_to_delete)
        borrowings = BorrowTool.objects.filter(user=user_to_delete)

        context["tools_responsible"] = tools_responsible
        context["borrowings"] = borrowings
        context["has_dependencies"] = tools_responsible.exists() or borrowings.exists()

        return context

    def test_func(self):
        return is_admin(self.request.user)

    def dispatch(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if user_to_delete == request.user:
            messages.error(self.request, "Vous ne pouvez pas supprimer votre propre compte.")
            return redirect("users:listUser")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        messages.success(self.request, f"L'utilisateur '{user_to_delete.username}' a été supprimé avec succès.")
        return super().delete(request, *args, **kwargs)
