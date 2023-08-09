from django.contrib import admin
from django.db import models
from ckeditor.widgets import CKEditorWidget
from .models import Course, Category, UserEnrollment, Review


class CourseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }


admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
admin.site.register(UserEnrollment)
admin.site.register(Review)
