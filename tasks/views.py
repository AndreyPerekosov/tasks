from django.http import HttpResponse
from django.shortcuts import redirect, render

from tasks.models import TodoItem
from tasks.forms import  TodoItemForm, TodoItemExportForm

#импортируем классы обработчики
from django.views import View
from django.views.generic import ListView

#3. импортируем модуль для работы с именами путей, вместо самих путей
from django.urls import reverse

#4. Импорт класса для отображения деталей задачи
from django.views.generic.detail import DetailView

#5. Добавляем требование авторизации
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q

from django.views import View

from django.core.mail import send_mail
from django.conf import settings



#5
@login_required
def index(request):
    return HttpResponse("Примитивный ответ из приложения tasks")

def complete_task(request, uid):
    t = TodoItem.objects.get(id=uid)
    t.is_completed = True
    t.save()
    return HttpResponse("OK")


def delete_task(request, uid):
    t = TodoItem.objects.get(id=uid)
    t.delete()
    #3.return redirect("/tasks/list")    
    return redirect(reverse("tasks:list"))


#2. заменяем функцию обработчик на класс обработчик     
# def task_create(request):
#     if request.method == "POST":
#         form = TodoItemForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/tasks/list")
#     else:
#         form = TodoItemForm()

#     return render(request, "tasks/create.html", {"form": form})

class TaskCreateView(View):
    def my_render(self, request, form):
        return render(request, "tasks/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = TodoItemForm(request.POST)
        if form.is_valid():
            # form.save()
            # return redirect("tasks:list")
            #добавляем владельца задачи
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect(reverse("tasks:list"))

        return self.my_render(request, form)

    def get(self, request, *args, **kwargs):
        form = TodoItemForm()
        return self.my_render(request, form)

# 1. больше не нужно, т.к. вынесли логику POST (создания задачи) в "обработчик" (функцию) task_create
# def add_task(request):
#     if request.method == "POST":
#         desc = request.POST["description"]
#         t = TodoItem(description=desc)
#         t.save()
#     return redirect("/tasks/list")
   
# 2. заменяем функцию обработчик на класс обработчик 
# def tasks_list(request):
#     all_tasks = TodoItem.objects.all()
#     return render(
#         request,
#         'tasks/list.html',
#         {'tasks': all_tasks}
#     )

class TaskListView(LoginRequiredMixin, ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"
    
    #первый способ получения всех тасок юзера
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     u = self.request.user
    #     if u.is_anonymous:
    #         return []
    #     return qs.filter(owner=u)
    #второй способ получения всех тасок юзера через "обратное отношение" которое было задано у модели
    def get_queryset(self):
        u = self.request.user
        #ниже строчки убрали, т.к. подмешали класс по проверке валидации пользователя
        # if u.is_anonymous:
        #     return []
        return u.tasks.all()
#4.
class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = 'tasks/details.html'

class TaskEditView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        t = TodoItem.objects.get(id=pk)
        form = TodoItemForm(request.POST, instance=t)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect(reverse("tasks:list"))

        return render(request, "tasks/edit.html", {"form": form, "task": t})

    def get(self, request, pk, *args, **kwargs):
        t = TodoItem.objects.get(id=pk)
        form = TodoItemForm(instance=t)
        return render(request, "tasks/edit.html", {"form": form, "task": t})

class TaskExportView(LoginRequiredMixin, View):
    def generate_body(self, user, priorities):
        q = Q()
        if priorities["prio_high"]:
            q = q | Q(priority=TodoItem.PRIORITY_HIGH)
        if priorities["prio_med"]:
            q = q | Q(priority=TodoItem.PRIORITY_MEDIUM)
        if priorities["prio_low"]:
            q = q | Q(priority=TodoItem.PRIORITY_LOW)
        tasks = TodoItem.objects.filter(owner=user).filter(q).all()

        body = "Ваши задачи и приоритеты:\n"
        for t in list(tasks):
            if t.is_completed:
                body += f"[x] {t.description} ({t.get_priority_display()})\n"
            else:
                body += f"[ ] {t.description} ({t.get_priority_display()})\n"

        return body

    def post(self, request, *args, **kwargs):
        form = TodoItemExportForm(request.POST)
        if form.is_valid():
            email = request.user.email
            body = self.generate_body(request.user, form.cleaned_data)
            send_mail("Задачи", body, settings.EMAIL_HOST_USER, [email])
            messages.success(
                request, "Задачи были отправлены на почту %s" % email)
        else:
            messages.error(request, "Что-то пошло не так, попробуйте ещё раз")
        return redirect(reverse("tasks:list"))

    def get(self, request, *args, **kwargs):
        form = TodoItemExportForm()
        return render(request, "tasks/export.html", {"form": form})