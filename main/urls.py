from django.urls import path
from main.views import (
    TaskListView, 
    about, 
    TaskCreateView, 
    TaskDetailView, 
    TaskUpdateView, 
    TaskDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    pin_comment
)

urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('about-us', about, name='about'),
    path('create', TaskCreateView.as_view(), name='create'),
    path('task/<int:pk>', TaskDetailView.as_view(), name='tasks-detail'),
    path('task/<int:pk>/update', TaskUpdateView.as_view(), name='tasks-update'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='tasks-delete'),
    path('task/<int:pk>/comment', CommentCreateView.as_view(), name='comment'),
    path('update_comment/<int:pk>', CommentUpdateView.as_view(), name='comment-update'), 
    path('delete_comment/<int:pk>', CommentDeleteView.as_view(), name='comment-delete'),
    path('pin-comment/<int:task_id>/<int:comment_id>/', pin_comment, name='pin-comment'),
]
