from django.urls import path
from homeservice import views

urlpatterns = [
    path("", views.home, name="home"),
] 