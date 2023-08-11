from django.urls import path
from . import views

urlpatterns = [
    path('courses', views.Courses.as_view(), name='courses'),
    path('course/<int:course_id>', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/review', views.review, name='review'),
    path('/course/API/', views.CourseAPI.as_view(), name='API_course_list'),
    path('/course/API/<int:course_id>', views.CourseAPI.as_view(), name='API_course_detail')
]
