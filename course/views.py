from django.views import View
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache

from .models import Course, Category, UserEnrollment, LEVEL_CHOICES
from checkout.models import CartItems

from utils.get_all_courses import get_all_courses
from .forms import ReviewForm

from django.db.models import Q
import random


class Courses(View):
    def get(self, request):
        current_page = self.paginator(request, get_all_courses())
        courses = current_page.object_list
        context = {
            'courses': [],
            'categories': Category.objects.all(),
            'levels': LEVEL_CHOICES,
            'current_page': current_page
        }
        for course in courses:
            context['courses'].append({
                'course': course,
                'categories': course.categories.all(),
                'course_enrolled_users': UserEnrollment.objects.filter(course=course).count()
            })
        return render(request, 'course/courses.html', context)

    def post(self, request):
        courses = get_all_courses()

        search_query = request.POST.get('search_query')
        if search_query:
            courses = courses.filter(
                Q(name__icontains=search_query) |
                Q(categories__name__icontains=search_query) |
                Q(level__icontains=search_query)
            ).distinct()

        checked_categories = request.POST.getlist('categories')
        categories = []
        for id in checked_categories:
            categories.append(int(id))

        checked_levels = request.POST.getlist('levels')
        levels = []
        for id in checked_levels:
            levels.append(int(id))

        price = request.POST.get('price')
        duration = request.POST.get('duration')

        if categories:
            courses = courses.filter(categories__id__in=categories)

        if levels:
            courses = courses.filter(level__in=levels)

        if price:
            courses = courses.filter(price__lte=int(price))

        if duration:
            courses = courses.filter(duration__lte=int(duration))

        current_page = self.paginator(request, courses)
        courses = current_page.object_list
        context = {
            'courses': [],
            'categories': Category.objects.all(),
            'levels': LEVEL_CHOICES,
            'current_page': current_page,
            'search_query': search_query,
            'selected_category': categories,
            'selected_levels': levels,
            'selected_price': price,
            'selected_duration': duration,
        }
        for course in courses:
            context['courses'].append({
                'course': course,
                'categories': course.categories.all(),
                'course_enrolled_users': UserEnrollment.objects.filter(course=course).count()
            })
        return render(request, 'course/courses.html', context)

    def paginator(self, request, courses):
        items_per_page = 10
        paginator = Paginator(courses, items_per_page)
        page_number = request.GET.get('page')
        if page_number is None:
            page_number = '1'

        try:
            current_page = paginator.page(int(page_number))
        except EmptyPage:
            current_page = paginator.page(paginator.num_pages)
        return current_page


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = ReviewForm()
    context = {
        'form': form,
        'course': course,
        'is_enrolled': False,
        'in_cart': False,
        'categories': course.categories.all(),
        'course_enrolled_users': UserEnrollment.objects.filter(course=course).count(),
        'instructor_enrolled_users': UserEnrollment.objects.filter(course__instructor=course.instructor).count(),
        'reviews': course.review_set.all(),
        'related_courses': []
    }
    related_courses = Course.objects.filter(categories__in=course.categories.all()).exclude(id=course.id).all()
    for related_course in random.sample(list(related_courses), min(3, len(list(related_courses)))):
        context['related_courses'].append({
            'course': related_course,
            'categories': related_course.categories.all(),
            'course_enrolled_users': UserEnrollment.objects.filter(course=related_course).count(),
        })
    if request.user.is_authenticated:
        context['is_enrolled'] = UserEnrollment.objects.filter(user=request.user, course=course).exists()

    cart = cache.get(f'cart_session_{request.session.session_key}')
    if CartItems.objects.filter(cart=cart, course=course).exists():
        context['in_cart'] = True

    return render(request, 'course/course_detail.html', context)


def review(request, course_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.instance.course = Course.objects.get(id=course_id)
            form.instance.user = request.user
            form.save()
            return redirect('course_detail', course_id=course_id)
        else:
            return Http404
    else:
        return Http404
