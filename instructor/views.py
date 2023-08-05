from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import User
from course.models import UserEnrollment
from .models import Instructor


def instructors(request):
    context = {
        'instructors': []
    }
    for instructor in Instructor.objects.all():
        context['instructors'].append({
            'instructor': instructor,
            'instructor_courses': instructor.course_set.count(),
            'enrolled_courses': User.objects.filter(enrollments__course__in=instructor.course_set.all()).count()
        })
    return render(request, 'instructor/instructors.html', context)


def instructor_profile(request, instructor_id):
    instructor = Instructor.objects.get(id=instructor_id)
    context = {
        'instructor': instructor,
        'courses': [],
        'courses_number': instructor.course_set.count(),
        'courses_enrolled': User.objects.filter(enrollments__course__in=instructor.course_set.all()).count(),
    }
    for course in instructor.course_set.all():
        context['courses'].append({
            'course': course,
            'categories': course.categories.all(),
            'course_enrolled_users': UserEnrollment.objects.filter(course=course).count(),
        })
    return render(request, 'instructor/instructor_profile.html', context)


@login_required
def instructor_group(request):
    if request.user.groups.filter(name='Instructors').exists():
        messages.error(request, 'نقش مدرس قبلا به حساب شما اضافه شده.')
        return redirect('dashboard')

    instructors_group = Group.objects.get(name='Instructors')
    request.user.groups.add(instructors_group)
    request.user.save()

    messages.info(request, 'نقش مدرس به حساب شما اضافه شد.')
    return redirect('dashboard')
