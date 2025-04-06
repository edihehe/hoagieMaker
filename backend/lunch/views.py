from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from datetime import date
from .models import StudentProfile
from .utils import is_lunch_period_valid, get_current_period

def is_teacher(user):
    return user.is_staff  # Assuming teachers are marked as staff

# @user_passes_test(is_teacher)
def teacher_dashboard(request):
    """Displays students' lunch schedules and allows teachers to update them."""
    students = StudentProfile.objects.all()
    current_period = get_current_period()
    today = date.today()
    
    # Filter students who currently have lunch
    students_with_lunch = [s for s in students if is_lunch_period_valid(s.user, current_period)]
    students_with_temp_permission = [s for s in students if s.temporary_permission == today]
    grab_and_go_students = [s for s in students if s.lunch_period == 0]
    
    return render(request, 'teacher_dashboard.html', {
        'students': students,
        'students_with_lunch': students_with_lunch,
        'students_with_temp_permission': students_with_temp_permission,
        'grab_and_go_students': grab_and_go_students,
        'current_period': current_period,
    })

# @user_passes_test(is_teacher)
def update_lunch_period(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == 'POST':
        lunch_period = request.POST.get('lunch_period')
        # Validate the lunch period is in the allowed choices
        valid_periods = [str(choice[0]) for choice in StudentProfile.LUNCH_PERIODS]
        if lunch_period in valid_periods:
            student.lunch_period = int(lunch_period)
            student.save()
            messages.success(request, 'Lunch period updated successfully!')
        else:
            messages.error(request, 'Invalid lunch period selected.')
    return redirect('teacher_dashboard')
# @user_passes_test(is_teacher)
def grant_temporary_permission(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    today = date.today()
    try:
        # Grant permission for today
        student.temporary_permission = today
        student.save()
        messages.success(request, f"Temporary permission granted for {student.user.get_full_name()} for today.")
    except Exception as e:
        messages.error(request, f"Error granting permission: {str(e)}")
    return redirect('teacher_dashboard')

def revoke_temporary_permission(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    try:
        # Set temporary_permission to None to revoke
        student.temporary_permission = None
        student.save()
        messages.success(request, f"Temporary permission revoked for {student.user.get_full_name()}.")
    except Exception as e:
        messages.error(request, f"Error revoking permission: {str(e)}")
    return redirect('teacher_dashboard')