from django.urls import path
from gymadmin import views

urlpatterns = [
    path("dashboard", views.dashboard),
]