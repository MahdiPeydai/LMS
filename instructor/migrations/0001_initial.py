# Generated by Django 4.2.3 on 2023-07-24 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import instructor.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='media/images/instructor/', validators=[instructor.models.validate_image_size])),
                ('short_description', models.TextField(max_length=200)),
                ('biography', models.TextField()),
                ('job_title', models.CharField(max_length=30)),
                ('user', models.ForeignKey(limit_choices_to={'groups': 2}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'instructor',
            },
        ),
    ]