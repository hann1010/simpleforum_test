from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    club = models.CharField(max_length=200, blank=True)
    call = models.CharField(max_length=200, blank=True)
    qth = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    town = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    user_level= models.IntegerField(default=1)
    list_rows= models.IntegerField(default=10)
    items_in_page= models.IntegerField(default=10)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    def __str__(self):
        return  str(self.user) + " / " + self.club +" / " \
        + self.call + " / " + self.qth + " / " \
        + str(self.user_level)



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

