from . import views
from django.urls import path
from .views import (
    #PostListView,
    #PostDetailView,
    TopicCreateView,
    #PostUpdateView,
    #PostDeleteView
)

urlpatterns = [
	path('', views.home, name='forum-home'),
	path('latest/topic/', views.latest_topic, name='forum-latest_topic'),
	path('topic/new/', TopicCreateView.as_view(), name='forum_topic-create'),
	
]