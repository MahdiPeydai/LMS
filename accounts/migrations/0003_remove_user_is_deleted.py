# Generated by Django 4.2.3 on 2023-07-19 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_user_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_deleted',
        ),
    ]
