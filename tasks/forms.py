from django import forms

from tasks.models import TodoItem

#генерация формы для заполнения
# class AddTaskForm(forms.Form):
#     description = forms.CharField(max_length=64, label="")

#модельная форма, связвается с моделью TodoItem
class TodoItemForm(forms.ModelForm):
    class Meta:
        model = TodoItem
        fields = ("description", "priority", "tags")
        labels = {"description": "Описание", "priority": "", "tags": "тэги"}

class TodoItemExportForm(forms.Form):
    prio_high = forms.BooleanField(
        label="высокая важность", initial=True, required=False
    )
    prio_med = forms.BooleanField(
        label="средней важности", initial=True, required=False
    )
    prio_low = forms.BooleanField(
        label="низкой важности", initial=False, required=False
    )