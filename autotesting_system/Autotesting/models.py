from django.db import models


class Institutions(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название института")

    def __str__(self):
        return self.name


class Specialties(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название специальности")
    institute = models.ForeignKey("Institutions", on_delete=models.PROTECT)


class Groups(models.Model):
    group_number = models.CharField(max_length=10, verbose_name="Номер группы")
    specialty = models.ForeignKey("Specialties", on_delete=models.PROTECT)


class Subjects(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")

    def __str__(self):
        return self.name


class SubjectsGroups(models.Model):
    subject = models.ForeignKey("Subjects", on_delete=models.PROTECT)
    group = models.ForeignKey("Groups", on_delete=models.PROTECT)


class Variants(models.Model):
    variant = models.IntegerField(verbose_name="Номер варианта")


class Students(models.Model):
    login = models.CharField(max_length=150, verbose_name="Логин студента", null=True) # null=True убрать нужно будет, в базе False
    group = models.ForeignKey("Groups", on_delete=models.PROTECT)
    variant = models.ForeignKey("Variants", on_delete=models.PROTECT, null=True) # убрать null=True
    points = models.IntegerField(verbose_name="Общее количество баллов студента", default=0)


class Laboratory_works(models.Model):
    title = models.CharField(max_length=100, verbose_name="Тема лабораторной работы")
    subject = models.ForeignKey("Subjects", on_delete=models.PROTECT)
    contest_id = models.IntegerField(verbose_name="Идентификатор контеста/лабы", null=True) # null=True убрать нужно будет, в базе False

    def __str__(self):
        return self.title


class Tasks(models.Model): 
    lab_work = models.ForeignKey("Laboratory_works", on_delete=models.PROTECT)
    contest_problem_id = models.CharField(max_length=50, verbose_name="ID задачи в контесте")
    name = models.CharField(max_length=150, verbose_name="Назание задачи")
    text = models.TextField(verbose_name="Текст задачи")
    input_data = models.TextField(verbose_name="Что на входе")
    output_data = models.TextField(verbose_name="Что на выходе")
    points = models.IntegerField(verbose_name="Кол-во баллов за задание", default=0)


class TasksVariants(models.Model):
    task = models.ForeignKey("Tasks", on_delete=models.PROTECT)
    variant = models.ForeignKey("Variants", on_delete=models.PROTECT)


class Solutions(models.Model):
    student = models.ForeignKey("Students", on_delete=models.PROTECT)
    task = models.ForeignKey("Tasks", on_delete=models.PROTECT)
    createAt = models.DateTimeField(verbose_name="Дата отправки решения")
    status = models.CharField(max_length=100, verbose_name="Статус решения")


# class Attempts(models.Model):
#     student = models.ForeignKey("Students", on_delete=models.PROTECT)
#     task = models.ForeignKey("Tasks", on_delete=models.PROTECT)
#     date_of_attempt = models.DateTimeField(verbose_name="Дата попытки")
#     text_of_attempt = models.TextField(verbose_name="Отчет о попытке")
#     comment = models.TextField(verbose_name="Комментарий преподавателя")


# class Test_type(models.Model):
#     test_type = models.CharField(max_length=10, verbose_name="Тип данных для тестов")


# class Tests(models.Model):
#     task = models.ForeignKey("Tasks", on_delete=models.CASCADE, null=True, blank=True)
#     test_type = models.ForeignKey("Test_type", on_delete=models.PROTECT)
#     data = models.TextField(verbose_name="Данные для тестов")
    