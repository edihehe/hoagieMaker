from django.urls import path
from . import views

urlpatterns = [
    path("success/<int:order_id>/", views.order_success, name="order_success"),
]
