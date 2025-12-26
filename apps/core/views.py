from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse


def home_view(request):
    return render(request, "home.html")


def no_permission(request):
    return render(request, "no-permission.html")


def create_superuser_once(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        return HttpResponse("Superuser created")
    return HttpResponse("Already exists")
