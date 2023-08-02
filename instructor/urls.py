from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    path('instructors', cache_page(60000)(views.instructors), name='instructors'),
    path('instructor/<int:instructor_id>', views.instructor_profile, name='instructor_profile'),
    path('user/group/store/instructor', views.instructor_group, name='add_instructor_group')
]
