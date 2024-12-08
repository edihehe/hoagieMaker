from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_list, name="menu_list"),
    path("create/", views.menu_create, name="menu_create"),
    path("<int:pk>/update/", views.menu_update, name="menu_update"),
    path("<int:pk>/", views.menu_detail, name="menu_detail"),
    path("<int:pk>/delete/", views.menu_delete, name="menu_delete"),
    path("delete-topping/", views.delete_topping, name="delete_topping"),
]
