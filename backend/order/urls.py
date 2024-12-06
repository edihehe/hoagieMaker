from django.urls import path
from . import views

urlpatterns = [
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("orders/", views.view_orders, name="view_orders"),
    path(
        "mark_completed/<int:order_id>/",
        views.mark_order_completed,
        name="mark_order_completed",
    ),
]
