# Generated by Django 4.1.3 on 2022-11-19 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_class_studio_class_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='studio',
        ),
        migrations.RemoveField(
            model_name='class',
            name='users',
        ),
    ]
