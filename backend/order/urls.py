from django.urls import path
from .views import *

urlpatterns = [
    path("", view_orders, name="view_orders"),
    path("<int:order_id>/",order_detail, name="order_detail"),
    path("success/<int:order_id>/", order_success, name="order_success"),
    path("deletes/<int:order_id>/", delete_order, name="delete_order"),
    path("delete/<int:order_id>/", kitchen_delete_order, name="kitchen_delete_order"),
    path(
        "mark_completed/<int:order_id>/",
        mark_order_completed,
        name="mark_order_completed",
    ),
]
