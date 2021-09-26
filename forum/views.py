from django.shortcuts import render
from .models import Forum_post
from django.contrib import messages
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
    success_url = '/latest/topic/'
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
        messages.add_message(self.request, messages.INFO, 'Yours new topic has been saved!')
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Forum_post
    success_url = '/latest/topic/'
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_context"] = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        return context

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/comment_new.html'
        else:
            template_name = ''
        return template_name

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'Comment'
        messages.add_message(self.request, messages.INFO, 'Yours new comment has been saved!')
        return super().form_valid(form)
