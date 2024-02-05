from django.shortcuts import render


# def index(request):
#     return HttpResponse("Hello, world. You're at the cumaweb index.")


def index(request):
    return render(request, "cumaweb/index.html")
