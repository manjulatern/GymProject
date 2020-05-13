from django.urls import path
from gyms import views

urlpatterns = [
    path("", views.index),
    path("login/", views.login),
    path("register/", views.register),
    path("activate/", views.activate),
    path("profile/", views.profile),
    path("profile/image", views.profile_image),
    path("logout/", views.logout),
]