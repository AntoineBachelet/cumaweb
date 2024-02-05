from django.shortcuts import render

from .models import AgriculturalTool


# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the catalog index.")


def index(request):
    all_tools = AgriculturalTool.objects.all()
    return render(request, "catalog/index.html", {"all_tools": all_tools})


# get_object_or_404
# si outil pas disponible pour utilisateur le renvoyer
