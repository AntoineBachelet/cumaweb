from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import CreateUserForm


def createUser(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CreateUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_user = User.objects.create_user(form.cleaned_data["login"], form.cleaned_data["email"], form.cleaned_data["password"])
            new_user.last_name = form.cleaned_data["lastname"]
            new_user.first_name = form.cleaned_data["firstname"]
            new_user.save()
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateUserForm()

    return render(request, "users/createUser.html", {"form": form})