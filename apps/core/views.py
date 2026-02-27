from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    return render(request, "home.html")


def no_permission(request):
    return render(request, "no-permission.html")


def health_check(request):
    return HttpResponse("OK")
