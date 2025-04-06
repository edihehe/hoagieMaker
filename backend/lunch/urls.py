from django.urls import path
from .views import *

urlpatterns = [
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('update-lunch/<int:student_id>/', update_lunch_period, name='update_lunch_period'),
    path('grant-permission/<int:student_id>/', grant_temporary_permission, name='grant_temporary_permission'),
    path('revoke-temp-permission/<int:student_id>/', revoke_temporary_permission, name='revoke_temporary_permission'),
]
