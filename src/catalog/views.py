"""Definition of views for catalog application"""

import datetime
from typing import Any

import openpyxl
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .forms import BorrowToolForm, CreateToolForm, ToolAccessForm
from .models import AgriculturalTool, BorrowTool, ToolAccess


class ToolListView(LoginRequiredMixin, ListView):
    """View to display the list of AgriculturalTool"""

    login_url = "/users/login"
    model = AgriculturalTool
    context_object_name = "all_tools"
    template_name = "catalog/index.html"

    def get_queryset(self):
        user = self.request.user
        accessible_tools = (AgriculturalTool.objects.filter(user_accesses__user=user) | AgriculturalTool.objects.filter(
            user=user
        )).distinct()
        return accessible_tools

class ToolAccessListView(LoginRequiredMixin, ListView):
    """View to display the list of AgriculturalTool"""

    login_url = "/users/login/"
    model = ToolAccess
    context_object_name = "all_accesses"
    template_name = "catalog/tool_access_list.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        tool = self.kwargs.get("tool_id")
        tool_object = AgriculturalTool.objects.get(id=tool)
        context["tool"] = tool_object
        return context

    def get_queryset(self):
        tool = self.kwargs.get("tool_id")
        tool_accesses = ToolAccess.objects.filter(tool = tool)
        return tool_accesses


class BorrowCreateView(LoginRequiredMixin, CreateView):
    """View to display BorrowToolForm"""

    login_url = "/users/login"
    form_class = BorrowToolForm
    model = BorrowTool
    template_name = "catalog/toolform.html"
    success_url = reverse_lazy("catalog:index")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["tool"] = get_object_or_404(AgriculturalTool, pk=self.kwargs.get("tool_id"))
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial["tool"] = get_object_or_404(AgriculturalTool, pk=self.kwargs.get("tool_id"))
        return initial

    def form_valid(self, form):
        messages.success(self.request, "L'utilisation de l'outil est bien enregistrée. Merci !")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Il y a une erreur dans le formulaire. Merci de vérifier les informations.")

        # Ajouter des messages spécifiques pour chaque erreur de champ
        for field, errors in form.errors.items():
            for error in errors:
                field_name = form.fields[field].label or field
                messages.error(self.request, f"Erreur dans le champ '{field_name}': {error}")

        return super().form_invalid(form)


class ToolDetailView(LoginRequiredMixin, DetailView):
    """View to display the detail of an AgriculturalTool"""

    login_url = "/users/login"
    model = AgriculturalTool
    context_object_name = "tool"
    template_name = "catalog/tooldetail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Get all borrows for this tool, ordered by most recent first
        context["borrows"] = BorrowTool.objects.filter(tool=self.object).order_by("-date_borrow", "-start_time_borrow")
        return context


class ToolUpdateView(LoginRequiredMixin, UpdateView):
    """View to display CreateToolForm"""

    login_url = "/users/login"
    form_class = CreateToolForm
    model = AgriculturalTool
    template_name = "catalog/createtoolform.html"
    success_url = reverse_lazy("catalog:index")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, "Outil mis à jour avec succès")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Il y a une erreur dans le formulaire. Merci de vérifier les informations.")
        return super().form_invalid(form)


class ToolCreateView(LoginRequiredMixin, CreateView):
    """View to display CreateToolForm"""

    login_url = "/users/login"
    form_class = CreateToolForm
    model = AgriculturalTool
    template_name = "catalog/createtoolform.html"
    success_url = reverse_lazy("catalog:index")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_initial(self):
        initial = super().get_initial()
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Nouvel outil enregistré")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        messages.error(self.request, "Il y a une erreur dans le formulaire. Merci de vérifier les informations.")
        return super().form_invalid(form)


class ToolAccessCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to display ToolAccessForm"""

    model = ToolAccess
    form_class = ToolAccessForm
    template_name = "catalog/tool_access_form.html"

    def test_func(self):
        """Check if user is the owner of the tool or is staff with UserPassesTestMixin"""
        tool = get_object_or_404(AgriculturalTool, pk=self.kwargs.get("tool_id"))
        return self.request.user == tool.user or self.request.user.is_staff

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["tool"] = get_object_or_404(AgriculturalTool, pk=self.kwargs.get("tool_id"))
        return kwargs

    def form_valid(self, form):
        form.instance.tool = get_object_or_404(AgriculturalTool, pk=self.kwargs.get("tool_id"))
        messages.success(self.request, f"Accès accordé à {form.instance.user.username}")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("catalog:tool_access_list", kwargs={'tool_id': self.kwargs.get('tool_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tool"] = get_object_or_404(AgriculturalTool, pk=self.kwargs.get("tool_id"))
        return context
    
class ToolAccessDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View to delete access to a tool"""
    model = ToolAccess
    template_name = 'catalog/tool_access_confirm_delete.html'
    
    def test_func(self):
        tool_access = self.get_object()
        return self.request.user == tool_access.tool.user or self.request.user.is_staff
    
    def get_success_url(self):
        messages.success(self.request, f"Accès retiré pour {self.object.user.username}")
        return reverse_lazy('catalog:tool_access_list', kwargs={'tool_id': self.object.tool.id})


def export_to_excel(request, tool_id):
    """Function to export to Excel the list of borrows for a given tool"""
    # Get the tool
    tool = get_object_or_404(AgriculturalTool, pk=tool_id)

    # Get all borrows for this tool
    borrows = BorrowTool.objects.filter(tool=tool).order_by("-date_borrow", "-start_time_borrow")

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Set headers
    worksheet["A1"] = "Nom Prénom"
    worksheet["B1"] = "Date"
    worksheet["C1"] = "Heure début"
    worksheet["D1"] = "Heure fin"
    worksheet["E1"] = "Durée (heures)"
    worksheet["F1"] = "Nom"
    worksheet["G1"] = "Total Heures par Personne"

    # Fill data
    row = 2
    for borrow in borrows:
        # Get full name or username
        full_name = borrow.user.get_full_name() if borrow.user.get_full_name() else borrow.user.username

        # Get start and end times
        start_time = borrow.start_time_borrow
        end_time = borrow.end_time_borrow

        duration = end_time - start_time

        worksheet[f"A{row}"] = full_name
        worksheet[f"B{row}"] = borrow.date_borrow.strftime("%d/%m/%Y")
        worksheet[f"C{row}"] = start_time
        worksheet[f"D{row}"] = end_time
        worksheet[f"E{row}"] = duration

        row += 1

    # Get unique names
    distinct_names = set()
    for borrow in borrows:
        distinct_names.add(borrow.user.get_full_name() if borrow.user.get_full_name() else borrow.user.username)

    # Add formulas for summing hours by person
    row = 2
    for name in distinct_names:
        worksheet[f"F{row}"] = name
        worksheet[f"G{row}"] = f'=SUMIFS(E:E, A:A, "{name}")'
        row += 1

    # Format the filename
    today = datetime.date.today().strftime("%d_%m_%Y")
    filename = f"{tool.name}_{today}.xlsx"

    # Prepare the response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Save the workbook to the response
    workbook.save(response)

    return response


# @login_required
