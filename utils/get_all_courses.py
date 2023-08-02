from django.core.cache import cache
from course.models import Course, UserEnrollment


def get_all_courses():
    courses = cache.get('all_courses')
    if not courses:
        courses = Course.objects.all()
        cache.set('all_courses', courses, 6000)
    return courses
