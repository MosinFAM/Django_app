from django.http import HttpResponse
from django.shortcuts import render, redirect
from main.forms import TaskForm
from main.models import Task
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, ListView, DetailView, CreateView, DeleteView
from django.urls import reverse_lazy


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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('home')

    template_name = 'main/task_delete.html'
 
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
     