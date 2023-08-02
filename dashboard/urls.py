from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/user/edit', views.ProfileEdit.as_view(), name='profile_edit'),
    path('password/edit', views.PasswordChange.as_view(), name='password_change'),
    path('courses', views.user_courses, name='user_courses'),
    path('courses/report', views.courses_report, name='instructor_course_report')
]
