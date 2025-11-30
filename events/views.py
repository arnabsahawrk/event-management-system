from django.shortcuts import render


# Create your views here.
def organizer_dashboard(request):
    return render(request, "dashboard/organizer-dashboard.html")
