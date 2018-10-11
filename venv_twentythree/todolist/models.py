from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Todo(models.Model):
    user = models.ForeignKey(User, related_name='wishes', on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    info = models.TextField(max_length=3000)
    todo_pic = models.ImageField(upload_to='media', blank=True)
    complete = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def meta_info_summary(self):
        len_info = len(self.info)
        if len_info > 480:
            return self.info[:480]+' . . . .continue'
        else:
            return self.info

    def meta_title_summary(self):
        len_title = len(self.title)
        if len_title >= 40:
            return self.title[:40]+'.....'
        else:
            return self.title

    def get_absolute_url(self):
        return reverse('todo:single', kwargs={'pk': self.pk, 'username': self.user.username})

    class Meta:
        ordering = ['-created_date']