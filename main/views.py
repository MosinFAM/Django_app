from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from main.forms import TaskForm, CommentForm
from main.models import Task, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# def home(request):
#     task = Task.objects.order_by('-id')
#     context = {
#         'title': 'Home page',
#         'tasks': task
#         }
#     return render(request, 'main/home.html', context=context)
    

class TaskListView(ListView):
    model = Task
    template_name = 'main/home.html'
    context_object_name = 'tasks'
    ordering = ['-date_posted']
    extra_context = {'title': 'Home page'}




def about(request):
    return render(request, 'main/about.html')


# def create(request):
#     error = ''
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         else:
#             error = "Form is not valid"

#     form = TaskForm()
#     context = {
#         'form': form,
#         'error': error
#     }
#     return render(request, 'main/create.html', context=context)



class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task

    form_class = TaskForm
    template_name = 'main/create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# def detailview(request, pk):
#     task = Task.objects.get(pk=pk)
#     context = {
#         'task': task
#         }
#     return render(request, 'main/details_view.html', context=context)


class TaskDetailView(DetailView):
    model = Task
    template_name = 'main/details_view.html'
    context_object_name = 'task'
    


# def updateview(request, pk):
#     task = Task.objects.get(pk=pk)

#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = TaskForm(instance=task)
        
#     context = {
#         'form': form,
#         'task': task
#     }
#     return render(request, 'main/task_update.html', context=context)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'main/task_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user 
        is_solved = self.request.POST.get('is_solved', False)
        if is_solved:
            form.instance.is_solved = True
        else:
            form.instance.is_solved = False
        return super().form_valid(form)


    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False
    

# def deleteview(request, pk):
#     task = Task.objects.get(pk=pk)
    
#     if request.method == 'POST':
#         task.delete()
#         return redirect('home')
    
#     context = {
#         'task': task
#                }
#     return render(request, 'main/task_delete.html', context=context)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')

    template_name = 'main/task_delete.html'
 
    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False
     
    

class CommentCreateView(LoginRequiredMixin, CreateView): 
    model = Comment 
    form_class = CommentForm 
    template_name = 'main/comment_add.html' 
 
    def form_valid(self, form): 
        task_id = self.kwargs.get('pk') 
        task = Task.objects.get(id=task_id) 
        form.instance.task = task 
        form.instance.author = self.request.user 
        return super().form_valid(form)  
    
 
    def get_success_url(self): 
        task_id = self.kwargs.get('pk') 
        return reverse_lazy('tasks-detail', kwargs={'pk': task_id})
    


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'main/comment_update.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False

    def get_success_url(self): 
        comment_id = self.kwargs.get('pk') 
        comment = Comment.objects.get(pk=comment_id)
        task_id = comment.task_id

        return reverse_lazy('tasks-detail', kwargs={'pk': task_id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'main/comment_delete.html'


    def test_func(self):
        task = self.get_object()
        if self.request.user == task.author:
            return True
        return False

    def get_success_url(self): 
        comment_id = self.kwargs.get('pk') 
        comment = Comment.objects.get(pk=comment_id)
        task_id = comment.task_id

        return reverse_lazy('tasks-detail', kwargs={'pk': task_id})



@login_required
def pin_comment(request, task_id, comment_id):
    task = get_object_or_404(Task, id=task_id)
    comment = get_object_or_404(Comment, id=comment_id, task=task)

    if task.author != request.user:
        return redirect('home')  # Перенаправляем пользователя, если он не является владельцем задачи

    # Снимаем закрепление со всех комментариев задачи
    for task_comment in task.comments.all():
        task_comment.is_pinned = False
        task_comment.save()

    # Закрепляем выбранный комментарий
    comment.is_pinned = True
    comment.save()

    return redirect('tasks-detail', pk=task_id)
    

    