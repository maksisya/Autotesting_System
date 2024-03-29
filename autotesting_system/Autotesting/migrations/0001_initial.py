# Generated by Django 4.2 on 2023-05-02 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_number', models.CharField(max_length=10, verbose_name='Номер группы')),
            ],
        ),
        migrations.CreateModel(
            name='Institutions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название института')),
            ],
        ),
        migrations.CreateModel(
            name='Laboratory_works',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100, verbose_name='Тема лабораторной работы')),
                ('max_points', models.IntegerField(verbose_name='Макс. кол-во баллов за ЛР')),
                ('num_of_tasks', models.IntegerField(verbose_name='Кол-во заданий в ЛР')),
                ('points_for_task', models.IntegerField(verbose_name='Кол-во баллов за задачу')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название предмета')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст задачи')),
                ('lab_work', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.laboratory_works')),
            ],
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.IntegerField(verbose_name='Номер варианта')),
            ],
        ),
        migrations.CreateModel(
            name='TasksVariants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.tasks')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.variants')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectsGroups',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.groups')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.subjects')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='ФИО студента')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.groups')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.variants')),
            ],
        ),
        migrations.CreateModel(
            name='Specialties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название специальности')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.institutions')),
            ],
        ),
        migrations.AddField(
            model_name='laboratory_works',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.subjects'),
        ),
        migrations.AddField(
            model_name='groups',
            name='specialty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Autotesting.specialties'),
        ),
    ]
