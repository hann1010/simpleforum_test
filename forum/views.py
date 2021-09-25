from django.shortcuts import render
from .models import Forum_post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    #ListView,
    #DetailView,
    CreateView,
    #UpdateView,
    #DeleteView,
)

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


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Forum_post
    success_url = '/'
    fields = ['title', 'content']

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/topic_new.html'
        else:
            template_name = ''
        return template_name

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'Topic'
        return super().form_valid(form)