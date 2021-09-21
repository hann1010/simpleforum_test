from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Forum_post(models.Model):
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_last_save = models.DateTimeField(auto_now=timezone.now)
    post_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.title + " / " + str(self.author)

