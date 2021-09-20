from . import views
from django.urls import path

urlpatterns = [
	path('', views.home, name='forum-home'),
	path('latest/topic/', views.latest_topic, name='forum-latest_topic'),
	
]