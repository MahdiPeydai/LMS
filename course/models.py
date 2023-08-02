from django.db import models
import os

from django.core.exceptions import ValidationError

from instructor.models import Instructor


def validate_image_size(value):
    max_size = 1024 * 1024

    if value.size > max_size:
        raise ValidationError(f"The maximum image size allowed is {max_size} bytes.")


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name


LEVEL_CHOICES = [
    (1, 'مبتدی'),
    (2, 'متوسط'),
    (3, 'پیشرفته'),
]


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=False)
    description = models.TextField(null=False)
    duration = models.IntegerField(null=False, help_text="ساعت")
    level = models.IntegerField(choices=LEVEL_CHOICES, null=False)
    image = models.ImageField(upload_to='media/images/course/', validators=[validate_image_size], null=False)
    price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField(Category, related_name='courses')

    class Meta:
        db_table = 'course'

    def delete(self, *args, **kwargs):
        if self.image:
            os.remove(self.image.path)
        super(Course, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name


class UserEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} : {self.course.name}"


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    message = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.course.name}): {self.message}"
