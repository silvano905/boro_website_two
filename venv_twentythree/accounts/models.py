from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profiles', on_delete=models.CASCADE)
    gender = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    profile_pic = models.ImageField(upload_to='media', blank=True)
    blocked_users = models.ManyToManyField('auth.User', related_name='blocked', blank=True, through='BlockedList')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.pk})


class BlockedList(models.Model):
    profile = models.ForeignKey(Profile, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
