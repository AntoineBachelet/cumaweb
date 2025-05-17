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

from .forms import CustomUserCreationForm, CustomUserEditForm


def is_admin(user):
    """Check if the user is an admin or a superuser"""
    return user.is_staff or user.is_superuser


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to create a new User"""

    login_url = "/users/login/"
    form_class = CustomUserCreationForm
    model = User
    template_name = "users/createUser.html"
    success_url = reverse_lazy("users:listUser")

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
    form_class = CustomUserEditForm
    template_name = 'users/createUser.html'
    success_url = reverse_lazy('users:listUser')
    
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
