from django.shortcuts import render


def home_view(request):
    return render(request, "home.html")


def no_permission(request):
    return render(request, "no-permission.html")
