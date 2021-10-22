#from _typeshed import Self
from django.shortcuts import render
from .models import Forum_post
from forum import models
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    #ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

def home(request):
    dic_x = {}
    if request.user.is_authenticated:
        list_rows_int = request.user.profile.list_rows
        db_data = Forum_post.objects.all().order_by('-date_posted')
        paginator = Paginator(db_data, list_rows_int)
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)
        dic_x = {
            'title': 'home',
            'posts': page_data
        }
    return render(request, 'forum/index.html', dic_x)


def latest_topics(request):
    dic_x = {}
    if request.user.is_authenticated:
        items_in_page_int = request.user.profile.items_in_page
        db_data = Forum_post.objects.filter(origin_post_id = 0).order_by('-date_posted')
        paginator = Paginator(db_data, items_in_page_int)
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)
        dic_x = {
            'title': 'latest topics',
            'posts': page_data
        }
    return render(request, 'forum/itemview.html', dic_x)


def latest_comments(request):
    dic_x = {}
    if request.user.is_authenticated:
        items_in_page_int = request.user.profile.items_in_page
        db_data = Forum_post.objects.exclude(origin_post_id = 0).order_by('-date_posted')
        paginator = Paginator(db_data, items_in_page_int)
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)
        dic_x = {
            'title': 'latest comments',
            'posts': page_data
        }
    return render(request, 'forum/itemview.html', dic_x)


def latest_all(request):
    dic_x = {}
    if request.user.is_authenticated:
        items_in_page_int = request.user.profile.items_in_page
        db_data = Forum_post.objects.all().order_by('-date_posted')
        paginator = Paginator(db_data, items_in_page_int)
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)
        dic_x = {
            'title': 'latest all',
            'posts': page_data
        }
    return render(request, 'forum/itemview.html', dic_x)


class AllDetailView(LoginRequiredMixin, DetailView): #Show one post
    model = Forum_post
    template_name = 'forum/oneview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'one post'
        return context


class ThreadDetailView(LoginRequiredMixin, DetailView): #Show post thread
    model = Forum_post
    template_name = 'forum/itemview.html'

    def get_context_data(self, **kwargs):
        items_in_page_int = self.request.user.profile.items_in_page
        context = super().get_context_data(**kwargs)
        db_data = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        if db_data['origin_post_id'] == 0:
            post_id = db_data['id']
        else:
            post_id = db_data['origin_post_id']
        db_data = Forum_post.objects.filter(Q(id = post_id) | Q(origin_post_id = post_id)).order_by('date_posted')
        paginator = Paginator(db_data, items_in_page_int)
        page_number = self.kwargs.get('page')
        page_data = paginator.get_page(page_number)
        context["posts"] = page_data
        context["title"] = 'message thread'
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_topics')
    fields = ['title', 'content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'new topic'
        return context

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/topic_new.html'
        else:
            template_name = 'forum/forbidden.html'
        return template_name

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_type = 'Topic'
        messages.add_message(self.request, messages.INFO, 'Yours new topic has been saved!')
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_comments')
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_context"] = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        context["title"] = 'new comment' 
        return context

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/comment_new.html'
        else:
            template_name = 'forum/forbidden.html'
        return template_name

    def form_valid(self, form):
        db_data = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.post_type = 'Comment'
        form.instance.title = 'Re: ' + db_data['title']
        if db_data['origin_post_id'] == 0:
            form.instance.origin_post_id = db_data['id']
        else:
            form.instance.origin_post_id = db_data['origin_post_id']
        info = 'Yours new comment to '+ db_data['title']+ ' has been saved!'
        messages.add_message(self.request, messages.INFO, info)
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_all')
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'edit post'
        return context

    def get_template_names(self):
        if  self.request.user.profile.user_level > 3:
            template_name = 'forum/edit_all.html'
        else:
            template_name = 'forum/forbidden.html'
        return template_name

    def form_valid(self, form):
        form.instance.author = self.request.user
        db_data = Forum_post.objects.all().values().get(pk=self.kwargs.get('pk'))
        info = 'Post '+ db_data['title']+ ' has been updated!'
        messages.add_message(self.request, messages.INFO, info)
        return super().form_valid(form)

    def test_func(self):
        Forum_post = self.get_object()
        if self.request.user == Forum_post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Forum_post
    success_url = reverse_lazy('forum-latest_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'delete post'
        return context

    def test_func(self):
        Forum_post = self.get_object()
        if self.request.user == Forum_post.author and self.request.user.profile.user_level > 4:
            return True
        return False 