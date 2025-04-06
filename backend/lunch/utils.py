from datetime import datetime

def is_lunch_period_valid(user, current_period):
    """Check if the student's lunch period matches the current period or if they have temporary permission."""
    if not hasattr(user, 'studentprofile'):
        return False  # Deny access if no StudentProfile exists

    student = user.studentprofile

    if student.has_temporary_permission():
        return True  # Allow ordering with temporary permission

    return student.lunch_period == current_period  # Check if it's their assigned lunch period

def get_current_period():
    """Returns the current school period (4-7) based on the time."""
    now = datetime.now().time()

    if now.hour >= 10 and now.hour < 11:  # Example: 4th period = 10:00 AM - 11:00 AM
        return 4
    elif now.hour >= 11 and now.hour < 12:
        return 5
    elif now.hour >= 12 and now.hour < 13:
        return 6
    elif now.hour >= 13 and now.hour < 14:
        return 7

    return 4  # No lunch period


