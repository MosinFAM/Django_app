from main.models import Task, Comment
from django.forms import ModelForm, TextInput, Textarea


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "task", "is_solved"]
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
        

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": Textarea(attrs={
                "placeholder": "Enter a comment",
                "class": "form-control"
            })
            }