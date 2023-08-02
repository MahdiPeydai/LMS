from django.views import View
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm, CustomPasswordChangeForm
from course.models import Course, UserEnrollment


@login_required
def dashboard(request):
    user = request.user
    context = {
        'user': user,
        'is_instructor': user.groups.filter(name='Instructors').exists()
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
        'is_instructor': user.groups.filter(name='Instructors').exists()
    }
    return render(request, 'dashboard/profile/profile.html', context)


class ProfileEdit(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form = UserUpdateForm(instance=user)
        context = {
            'user': user,
            'is_instructor': user.groups.filter(name='Instructors').exists(),
            'form': form
        }
        return render(request, 'dashboard/profile/profile_edit.html', context)

    @method_decorator(login_required)
    def post(self, request):
        method = self.request.POST.get('_method')
        if method == 'put':
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                return self.put(request, form=form)
            else:
                raise Http404
        elif method == 'delete':
            return self.delete(request)
        raise Http404

    @method_decorator(login_required)
    def put(self, request, form):
        form.save()
        messages.info(request, 'تغییرات با موفقیت ذخیره شد.')
        return redirect('profile')

    @method_decorator(login_required)
    def delete(self, request):
        return redirect('register')


class PasswordChange(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        form = CustomPasswordChangeForm(user=user)
        context = {
            'is_instructor': user.groups.filter(name='Instructors').exists(),
            'form': form
        }
        return render(request, 'dashboard/password_change/password_change.html', context)

    @method_decorator(login_required)
    def post(self, request):
        method = self.request.POST.get('_method')
        if method == 'put':
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                return self.put(request, form=form)
            else:
                messages.error(request, form.errors)
                return redirect('password_change')
        else:
            raise Http404

    @method_decorator(login_required)
    def put(self, request, form):
        user = form.save()
        update_session_auth_hash(request, user)

        messages.info(request, 'تغییرات با موفقیت ذخیره شد.')
        return redirect('password_change')


@login_required
def user_courses(request):
    user = request.user
    courses = Course.objects.filter(userenrollment__user=user)
    context = {
        'courses': [],
        'is_instructor': user.groups.filter(name='Instructors').exists(),
    }
    for course in courses:
        context['courses'].append({
            'course': course,
            'categories': course.categories.all(),
            'instructor': course.instructor,
        })
    return render(request, 'dashboard/courses/courses.html', context)


@login_required
def courses_report(request):
    user = request.user
    instructor_courses = Course.objects.filter(instructor__user=user)
    context = {
        'courses': []
    }
    for course in instructor_courses:
        context['courses'].append({
            'course': course,
            'enrolled_users': UserEnrollment.objects.filter(course=course).count(),
            'categories': course.categories.all(),
            'income': int(course.price * UserEnrollment.objects.filter(course=course).count()),
            'is_instructor': user.groups.filter(name='Instructors').exists(),
        })
    return render(request, 'dashboard/instructor_courses_report/instructor_courses_report.html', context)
