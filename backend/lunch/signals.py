from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

User = get_user_model()

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Automatically create a StudentProfile when a new user is created."""
    if created and not hasattr(instance, 'studentprofile'):
        from .models import StudentProfile  # Import inside function to avoid circular imports
        StudentProfile.objects.create(user=instance, lunch_period=4)  # Default to 4th period

@receiver(user_logged_in)
def ensure_student_profile_exists(sender, request, user, **kwargs):
    """Ensure the user has a StudentProfile when logging in."""
    if not hasattr(user, 'studentprofile'):
        from .models import StudentProfile  # Import inside function to avoid circular imports
        StudentProfile.objects.create(user=user, lunch_period=4)  # Default to 4th period
