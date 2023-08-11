from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import User


def validate_image_size(value):
    max_size = 1024 * 1024

    if value.size > max_size:
        raise ValidationError(f"The maximum image size allowed is {max_size} bytes.")


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"groups": 2})
    image = models.ImageField(upload_to='images/instructor/', validators=[validate_image_size], null=False)
    short_description = models.TextField(max_length=200, null=False)
    biography = models.TextField(null=False)
    job_title = models.CharField(max_length=30, null=False)

    class Meta:
        db_table = 'instructor'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
