from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from .models import AgriculturalTool, BorrowToolForm


# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the catalog index.")


def index(request):
    all_tools = AgriculturalTool.objects.all()
    return render(request, "catalog/index.html", {"all_tools": all_tools})


def see_tool(request, tool_id):
    if request.method == "POST":
        form = BorrowToolForm(request.POST)
        if form.is_valid():
            form.save()
            # update the rendering
            tool_id = form.cleaned_data["tool"].id
            tool = get_object_or_404(AgriculturalTool, pk=tool_id)
            user = User.objects.all()
            form = BorrowToolForm(initial={"tool": tool})
            messages.success(request, "L'utilisation de l'outil est bien enregistrée. Merci !")
            return render(request, "catalog/tool.html", {"tool": tool, "users": user, "form": form})
        else:
            messages.error(request, "Il y a une erreur dans le formulaire. Merci de vérifier les informations.")
            tool = get_object_or_404(AgriculturalTool, pk=tool_id)
            user = User.objects.all()
            form = BorrowToolForm(initial={"tool": tool})
            return render(request, "catalog/tool.html", {"tool": tool, "users": user, "form": form})
    else:
        tool = get_object_or_404(AgriculturalTool, pk=tool_id)
        # get all the user
        user = User.objects.all()
        # init form with the tool
        form = BorrowToolForm(initial={"tool": tool})
        return render(request, "catalog/tool.html", {"tool": tool, "users": user, "form": form})


# def get_borrowed(request):
#     """check if the form is valid and save it, the update the rendering of the page with a json message"""
#     if request.method == "POST":
#         pass


# pré remplir le format du jour en le forcant

# def get_borrowed(request):
#     # avoir id du modele autrement que par le formulaire peut être
#     if request.method == "POST":
#         form = BorrowToolForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # update the rendering
#             tool_id = form.cleaned_data["tool"].id
#             tool = get_object_or_404(AgriculturalTool, pk=tool_id)
#             user = User.objects.all()
#             see_tool(request, form.cleaned_data["tool"].id)
#     else:
#         return see_tool(request, form.cleaned_data["tool"].id)

# pré remplir le format du jour en le forcant

# @login_required
