from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='1')

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse("task", kwargs={"pk": self.pk})
    
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'