from django.core.cache import cache
from course.models import Course, UserEnrollment
from django.db.models import Count


def get_offer_courses():
    offer_courses = cache.get('offer_courses')
    if not offer_courses:
        offer_courses_query = Course.objects.annotate(num_enrollments=Count('enrollments')).order_by('num_enrollments')[
                              :6]
        offer_courses = []
        for course in offer_courses_query:
            offer_courses.append({
                'course': course,
                'categories': course.categories.all(),
                'course_enrolled_users': UserEnrollment.objects.filter(course=course).count(),
            })
        cache.set('offer_courses', offer_courses, 60)
    return offer_courses
