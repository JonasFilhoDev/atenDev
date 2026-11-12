"""URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'entrar/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login',
    ),
    path('sair/', auth_views.LogoutView.as_view(), name='logout'),
    path('atendimentos/', include('atendimentos.urls')),
    path(
        '',
        RedirectView.as_view(pattern_name='atendimentos:lista', permanent=False),
        name='home',
    ),
]
