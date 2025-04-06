from django.db import models
from django.contrib.auth.models import User
from datetime import date

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Lunch periods (4th to 7th)
    LUNCH_PERIODS = [
        (4, '4th Period'),
        (5, '5th Period'),
        (6, '6th Period'),
        (7, '7th Period'),
    ]

    lunch_period = models.IntegerField(choices=LUNCH_PERIODS, null=True, blank=True)

    # Temporary permission for a specific day (e.g., for exams)
    temporary_permission = models.DateField(null=True, blank=True)

    def has_temporary_permission(self):
        """Check if the student has permission to order outside their lunch period today."""
        return self.temporary_permission == date.today()

    def __str__(self):
        return f"{self.user.username} - {self.get_lunch_period_display()}"
