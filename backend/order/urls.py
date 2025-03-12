from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_orders, name="view_orders"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("delete/<int:order_id>/", views.delete_order, name="delete_order"),
    path(
        "mark_completed/<int:order_id>/",
        views.mark_order_completed,
        name="mark_order_completed",
    ),
]
