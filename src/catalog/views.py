from django.shortcuts import get_object_or_404, render

from .models import AgriculturalTool


# Create your views here.
# def index(request):
#     return HttpResponse("Hello, world. You're at the catalog index.")


def index(request):
    all_tools = AgriculturalTool.objects.all()
    return render(request, "catalog/index.html", {"all_tools": all_tools})


def see_tool(request, tool_id):
    tool = get_object_or_404(AgriculturalTool, pk=tool_id)
    return render(request, "catalog/tool.html", {"tool": tool})
