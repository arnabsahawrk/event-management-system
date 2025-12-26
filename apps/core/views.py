from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse


def home_view(request):
    return render(request, "home.html")


def no_permission(request):
    return render(request, "no-permission.html")


def bootstrap_admin(request):
    if User.objects.filter(username="admin").exists():
        return HttpResponse("Admin already exists")

    user = User.objects.create_superuser(
        username="admin", email="admin@example.com", password="1234"
    )

    admin_group, _ = Group.objects.get_or_create(name="Admin")
    user.groups.add(admin_group)

    return HttpResponse("Admin user created")
