from django.urls import path
from main.views import (
    TaskListView, 
    about, 
    TaskCreateView, 
    TaskDetailView, 
    TaskUpdateView, 
    PostDeleteView
)

urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('about-us', about, name='about'),
    path('create', TaskCreateView.as_view(), name='create'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='tasks-detail'),
    path('task/<int:pk>/update', TaskUpdateView.as_view(), name='tasks-update'),
    path('task/<int:pk>/delete', PostDeleteView.as_view(), name='tasks-delete'),
]
