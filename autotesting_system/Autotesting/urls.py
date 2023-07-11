from django.urls import path

from . import views

urlpatterns = [
    # path("lab_works/<int:lab_id>/", views.current_lab, name="current_lab"),
    # path("lab_works/", views.lab_works, name="lab_works"),
    # path("current_task/<int:task_id>/", views.current_task, name="current_task_info"),
    path("lab_works_list/<int:lab_id>/<int:task_id>/submissions_list/<int:run_id>/", views.current_run, name="current_run"),
    path("lab_works_list/<int:lab_id>/<int:task_id>/submissions_list/", views.submissions_list, name="submissions_list"),
    path("lab_works_list/<int:lab_id>/<int:task_id>/", views.current_task, name="current_task_info"),
    path("lab_works_list/<int:lab_id>/", views.current_lab, name="current_lab"),
    path("lab_works_list/", views.show_lab_works_list, name="lab_list"),
    # path(""),
    path("success_auth/", views.success_auth, name="success_auth"),
    path("auth/", views.auth, name="auth"),
    # path("contest_info/", views.contest_info, name="contest_info"),
    path("", views.main_page, name="main_page"),
]