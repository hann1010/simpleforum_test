from . import views
from django.urls import path
from .views import (
    #PostListView,
    #PostDetailView,
    TopicCreateView,
    CommentCreateView,
    #PostUpdateView,
    #PostDeleteView
)

from . import views

urlpatterns = [
    path('', views.home, name='forum-home'),
    path('latest/topics/', views.latest_topics, name='forum-latest_topics'),
    path('latest/comments/', views.latest_comments, name='forum-latest_comments'),
    path('latest/all/', views.latest_all, name='forum-latest_all'),
    path('topic/new/', TopicCreateView.as_view(), name='forum_topic-create'),
    path('all/<int:pk>/comment/new/', CommentCreateView.as_view(), name='forum_comment-create'),
	
]