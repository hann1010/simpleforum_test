from django.shortcuts import render

def home(request):
    dic_x = {
        'title': 'Home'
    }
    return render(request, 'forum/index.html', dic_x)
