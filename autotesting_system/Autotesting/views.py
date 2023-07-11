from django.shortcuts import redirect, render
from django.http import HttpResponse
# import json

from .forms import Submission

import requests

from .models import *


client_id = "e8e1362d1f984695902bc772ed2a7623"
client_secret = "" # секретный ключ приложения


def main_page(request):
    token = request.session.get("token")
    if token:
        return redirect("success_auth")
    return render(request, "Autotesting/main_page.html")


# Успешная авторизация
def success_auth(request):
    request.session.set_expiry(0)
    token = request.session.get("token")
    if not token:
        return redirect(f"https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id}"
                        f"&redirect_uri=http://127.0.0.1:8000/auth")
    user_info = requests.get("https://login.yandex.ru/info?", headers={"Authorization": f"OAuth {token}"}).json()
    return render(request, "Autotesting/success_auth.html",
                  context={"token": token, "user_fullname": user_info.get("real_name")})


# Авторизация
def auth(request):
    if request.GET.get("code"):
        code = request.GET.get("code")
        response = requests.post("https://oauth.yandex.ru/token",
                                 data={"grant_type": "authorization_code",
                                       "code": code, "client_id": client_id,
                                       "client_secret": client_secret
                                       }
                                 ).json()
        request.session["token"] = response.get("access_token")
        # получаем информацию о пользователе из api yandex ID
        response = requests.get("https://login.yandex.ru/info?",
                                headers={"Authorization": f"OAuth {request.session.get('token')}"}).json()
        student_login = response.get("login")
        # проверяем есть ли в базе залогинившийся студент
        if not Students.objects.filter(login=student_login):
            student = Students()
            student.login = student_login
            # для отладки работы студенты пока помещаются в одну группу, имеют один вариант
            student.group = Groups.objects.get(id=1)
            student.variant = Variants.objects.get(id=1)
            student.save()
        return redirect("/success_auth")
    return render(request, "Autotesting/success_auth.html")


# Отображение списка лабораторных работ
def show_lab_works_list(request):
    lab_list = Laboratory_works.objects.all()
    context = {
        "lab_list": lab_list
    }
    return render(request, "Autotesting/lab_works.html", context=context)


# Отображение информации о конкретной лабораторной работе
def current_lab(request, lab_id):
    task_list = Tasks.objects.filter(lab_work_id=lab_id)
    context = {
        "task_list": task_list
    }
    return render(request, "Autotesting/task.html", context=context)


# Отображение информации о конкретной задаче лабораторной работы
def current_task(request, lab_id, task_id):
    task_info = Tasks.objects.get(id=task_id, lab_work_id=lab_id)
    if request.method == "POST":
        form = Submission(request.POST, request.FILES)
        if form.is_valid():  # если данные в форме корректны
            file = request.FILES["file"]  # получаем инфу о загруженном в форму файле
            contest_id = task_info.lab_work.contest_id
            headers = {
                "Authorization": f"OAuth { request.session.get('token') }"  # определение заголовка для запросов
            }
            # получаем список задач в контесте (лабе)
            problems_response = requests.get(
                f"https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/problems",
                headers=headers).json()
            # извлекаем данные для попытки отправить решение
            # compiler = problems_response["problems"][task_id - 1]['compilers']
            # компилер захардкоден, потому что пока что все задачи только на Python
            
            current_problem = []

            for prob in problems_response["problems"]:
                if prob["id"] == task_info.contest_problem_id:
                    current_problem = prob
            
            compiler = current_problem["compilers"]
            problem = current_problem["alias"]

            files = {
                "file": file
            }
            data = {
                "compiler": compiler,
                "problem": problem
            }
            # при попытке отправить данный запрос, вылетает ошибка: problem not found.
            # для решения параметр problem нужно брать в запросе из problem.alias
            # не удается отправить запрос, потому что он не понимает какой именно файл я отправляю
            # нужно гуглить каким еще образом я могу передать файл в запрос
            # решение - файл нужно было передавать через параметр files запроса
            response = requests.post(f"https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/submissions",
                                     data=data, headers=headers, files=files).json()
            
            if response.get("runId"):
                con = {
                    "lab_id": lab_id,
                    "task_id": task_id,
                    "sumbission_id": response.get("runId")
                }
                return render(request, "Autotesting/success_submit.html", context=con)
            
            return HttpResponse("Ошибка отправки решения")
        
        return HttpResponse("Invalid data")
    else:
        form = Submission()
    
    context = {
        "task_info": task_info,
        "form": form
    }
    return render(request, "Autotesting/current_task.html", context=context)


def submissions_list(request, lab_id, task_id):
    headers = {"Authorization": f"OAuth {request.session.get('token')}"}
    task_info = Tasks.objects.get(id=task_id, lab_work_id=lab_id)
    contest_id = task_info.lab_work.contest_id
    
    # получаем инфу о студенте
    response = requests.get("https://login.yandex.ru/info?", headers=headers).json()
    student_login = response.get("login")

    # инфа о студенте в рамках участия в контесте
    participant_info = requests.get(
        f"https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/participants?login={student_login}",
        headers=headers).json()
    participant_id = participant_info[0]["id"]
    response = requests.get(
        f"https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/participants/{participant_id}/stats",
        headers=headers).json()

    # выбираем только те решения, которые соответствуют задаче
    runs = []

    for run in response["runs"]:
        if run["problemId"] == task_info.contest_problem_id:
            runs.append(run)

    context = {
        "runs": runs,
        "lab_id": lab_id,
        "task_id": task_id
    }
    return render(request, "Autotesting/submissions_list.html", context=context)


def current_run(request, lab_id, task_id, run_id):
    headers = {"Authorization": f"OAuth {request.session.get('token')}"}

    task_info = Tasks.objects.get(id=task_id, lab_work_id=lab_id)
    contest_id = task_info.lab_work.contest_id
    
    # получаем инфу о студенте
    response = requests.get("https://login.yandex.ru/info?", headers=headers).json()
    student_login = response.get("login")

    # инфа о студенте в рамках участия в контесте
    participant_info = requests.get(
        f"https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/participants?login={student_login}",
        headers=headers
    ).json()
    participant_id = participant_info[0]["id"]
    
    response = requests.get(
        f"https://api.contest.yandex.net/api/public/v2/contests/{contest_id}/participants/{participant_id}/stats",
        headers=headers
    ).json()
    
    # выбираем конкретную задачу
    current_run_info = None

    for run in response["runs"]:
        if run["runId"] == run_id:
            current_run_info = run
    
    if current_run_info:
        context = {
            "lab_id": lab_id,
            "task_id": task_id,
            "current_run_info": current_run_info
        }
        return render(request, "Autotesting/current_run_info.html", context=context)
    
    return HttpResponse("Run not found")
