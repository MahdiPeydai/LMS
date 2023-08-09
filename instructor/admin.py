from django.contrib import admin
from django.db import models
from .models import Instructor
from ckeditor.widgets import CKEditorWidget


class InstructorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }


admin.site.register(Instructor, InstructorAdmin)
