# Generated by Django 4.0.4 on 2023-06-11 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Autotesting', '0004_remove_tests_task_remove_tests_test_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='yandex_id',
        ),
    ]
