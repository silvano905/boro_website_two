from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class MakePost(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=63)
    post_pic = models.ImageField(upload_to='media', blank=True)
    info = models.TextField(max_length=3000)
    likes = models.ManyToManyField('auth.User', related_name='likes', blank=True, through='LikeUserList')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def post_info_summary(self):
        len_info = len(self.info)
        if len_info > 480:
            return self.info[:480]+' . . . .continue'
        else:
            return self.info

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_date']


class LikeUserList(models.Model):
    post = models.ForeignKey(MakePost, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username