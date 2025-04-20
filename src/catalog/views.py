"""Definition of views for catalog application"""

import datetime
from typing import Any

import openpyxl
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import BorrowToolForm, CreateToolForm
from .models import AgriculturalTool, BorrowTool


class ToolListView(LoginRequiredMixin, ListView):
    """View to display the list of AgriculturalTool"""

    login_url = "/users/login"
    model = AgriculturalTool
    context_object_name = "all_tools"
    template_name = "catalog/index.html"


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
        context["borrows"] = BorrowTool.objects.filter(tool=self.object).order_by("-date_borrow", "-time_borrow")
        return context


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


def export_to_excel(request, tool_id):
    """Function to export to Excel the list of borrows for a given tool"""
    # Get the tool
    tool = get_object_or_404(AgriculturalTool, pk=tool_id)

    # Get all borrows for this tool
    borrows = BorrowTool.objects.filter(tool=tool).order_by("-date_borrow", "-time_borrow")

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Set headers
    worksheet["A1"] = "Nom Prénom"
    worksheet["B1"] = "Date"
    worksheet["C1"] = "Heure"
    worksheet["D1"] = "Durée (heures)"
    worksheet["E1"] = "Nom"
    worksheet["F1"] = "Total Heures par Personne"

    # Fill data
    row = 2
    for borrow in borrows:
        # Get full name or username
        full_name = borrow.user.get_full_name() if borrow.user.get_full_name() else borrow.user.username

        # Convert time_borrow to decimal hours (assuming time_borrow is stored as 'HH:MM')
        time_hour = borrow.time_borrow.hour
        time_minute = borrow.time_borrow.minute
        time_decimal = time_hour + (time_minute / 60)

        worksheet[f"A{row}"] = full_name
        worksheet[f"B{row}"] = borrow.date_borrow.strftime("%d/%m/%Y")
        worksheet[f"C{row}"] = borrow.time_borrow.strftime("%H:%M")
        worksheet[f"D{row}"] = time_decimal

        row += 1

    # Get unique names
    distinct_names = set()
    for borrow in borrows:
        distinct_names.add(borrow.user.get_full_name() if borrow.user.get_full_name() else borrow.user.username)

    # Add formulas for summing hours by person
    row = 2
    for name in distinct_names:
        worksheet[f"E{row}"] = f"=A{row}"
        worksheet[f"F{row}"] = f'=SUMIFS(D:D, A:A, "{name}")'
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
