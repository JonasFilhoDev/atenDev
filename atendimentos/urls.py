"""Rotas do app atendimentos."""

from django.urls import path

from . import views

app_name = "atendimentos"

urlpatterns = [
    path("", views.lista, name="lista"),
]
