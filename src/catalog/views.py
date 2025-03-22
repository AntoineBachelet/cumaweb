from typing import Any

from django.contrib import messages
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import BorrowToolForm, CreateToolForm
from .models import AgriculturalTool, BorrowTool


class ToolListView(ListView):
    model = AgriculturalTool
    context_object_name = "all_tools"
    template_name = "catalog/index.html"


class BorrowCreateView(CreateView):
    form_class = BorrowToolForm
    model = BorrowTool
    template_name = "catalog/toolform.html"

    def get_success_url(self):
        return reverse_lazy("catalog:borrow_tool", kwargs={"tool_id": self.kwargs.get("tool_id")})

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
        return super().form_invalid(form)

class ToolCreateView(CreateView):
    form_class = CreateToolForm
    model = AgriculturalTool
    template_name = "catalog/createtoolform.html"

    def get_success_url(self):
        return reverse_lazy("catalog:create_tool")

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


# @login_required
