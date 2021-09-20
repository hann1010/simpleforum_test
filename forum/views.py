from django.shortcuts import render

def home(request):
    dic_x = {
        'title': 'home'
    }
    return render(request, 'forum/index.html', dic_x)


def latest_topic(request):
    dic_x = {
        'title': 'latest topic'
    }
    return render(request, 'forum/itemview.html', dic_x)