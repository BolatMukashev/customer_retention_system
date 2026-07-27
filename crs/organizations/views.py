from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ApplicationForm


def index(request):
    return HttpResponse("<h1>Добро пожаловать на страницу организаций!</h1>")


def apply(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("organizations:apply_success")
    else:
        form = ApplicationForm()

    return render(request, "organizations/application_form.html", {"form": form})


def apply_success(request):
    return render(request, "organizations/application_success.html")