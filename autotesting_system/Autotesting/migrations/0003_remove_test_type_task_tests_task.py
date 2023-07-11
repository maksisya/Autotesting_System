# Generated by Django 4.2 on 2023-06-01 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Autotesting', '0002_test_type_remove_laboratory_works_max_points_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_type',
            name='task',
        ),
        migrations.AddField(
            model_name='tests',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Autotesting.tasks'),
        ),
    ]