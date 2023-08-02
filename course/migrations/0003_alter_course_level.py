# Generated by Django 4.2.3 on 2023-07-27 00:02

from django.db import migrations, models


def convert_charfield_to_integer(apps, schema_editor):
    YourModel = apps.get_model('course', 'Course')
    for obj in YourModel.objects.all():
        obj.level = 1
        obj.save()


class Migration(migrations.Migration):
    dependencies = [
        ('course', '0002_auto_20230727_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.IntegerField(choices=[(1, 'مبتدی'), (2, 'متوسط'), (3, 'پیشرفته')]),
        ),
        migrations.RunPython(convert_charfield_to_integer)
    ]
