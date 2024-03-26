from main.models import Task
from django.forms import ModelForm, TextInput, Textarea


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task"]
        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Enter the title",
                "class": "form-control"
            }),
            "task": Textarea(attrs={
                "placeholder": "Enter a description",
                "class": "form-control"
            })
            }