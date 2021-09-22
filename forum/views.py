from django.shortcuts import render
from .models import Forum_post

def home(request):
    dic_x = {
        'title': 'home'
    }
    return render(request, 'forum/index.html', dic_x)


def latest_topic(request):
    dic_x = {}
    if request.user.is_authenticated:
        dic_x = {
            'title': 'latest topic',
            'posts' : Forum_post.objects.all().order_by('-date_posted')
        }
    return render(request, 'forum/itemview.html', dic_x)