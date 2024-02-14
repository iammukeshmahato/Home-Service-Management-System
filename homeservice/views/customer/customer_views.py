from django.shortcuts import render, HttpResponse, redirect
from homeservice.models import Service
from django.contrib.auth import logout


def home(request):
    return render(request, "customer/home.html")


def services(request):
    services = Service.objects.all()
    return render(request, "customer/services.html", {"services": services})


def service_details(request, slug):
    service = Service.objects.get(slug=slug)
    return render(request, "customer/service_details.html", {"service": service})
    return HttpResponse(slug)

def customer_logout(request):
    logout(request)
    return redirect("login")