# Generated by Django 4.2.3 on 2023-07-29 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_userenrollment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userenrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='course.course'),
        ),
    ]
