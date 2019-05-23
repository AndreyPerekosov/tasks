from django.urls import path

from . import views

#задаем namespace
app_name = "tasks"

urlpatterns = [
    path('', views.index, name='index'),
    # path('list/', views.tasks_list, name='list'), данные пути убираем, т.к. убрали функции-обработчики и заменили классами-обработчиками
    # path("create/", views.task_create, name="create"),
    # path("add-task/", views.add_task, name="api-add-task"), не нужен путь, т.к. убрали обработчик add_task
    path('complete/<int:uid>', views.complete_task, name='complete'),
    path('delete/<int:uid>', views.delete_task, name='delete'),
    #прописываем пути для классо обработчиков
    #path("list/", views.TaskListView.as_view(), name="list"),
    path("list/", views.tasks_by_tag, name="list"),
    path("list/tag/<slug:tag_slug>", views.tasks_by_tag, name="list_by_tag"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    path("details/<int:pk>", views.TaskDetailsView.as_view(), name="details"),
    path("edit/<int:pk>", views.TaskEditView.as_view(), name="edit"),
    path("export/", views.TaskExportView.as_view(), name="export"),
]