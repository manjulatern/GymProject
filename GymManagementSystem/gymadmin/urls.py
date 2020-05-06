from django.urls import path
from gymadmin import views

urlpatterns = [
    path("", views.dashboard),
]