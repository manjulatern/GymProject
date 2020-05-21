from django.urls import path
from gymadmin import views

urlpatterns = [
    path("", views.dashboard),
    path("gyms/createGym/", views.create_gym),
    path("gyms/", views.gyms),
    path("gyms/detail/<int:gym_id>",views.gym_details),
    path("gyms/delete/<int:gym_id>",views.gym_delete),
    path("gyms/edit/<int:gym_id>",views.edit_gym),
    path("gyms/updateGym/", views.update_gym),
]