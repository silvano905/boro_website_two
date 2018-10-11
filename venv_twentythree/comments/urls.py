from django.conf.urls import url
from comments import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'comments'

urlpatterns = [
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^todo/(?P<pk>\d+)/suggestion/$', views.add_suggestion_to_todo, name='add_suggestion_to_todo'),
    url(r'^commentsapi/$', views.CommentListAPI.as_view()),
    url(r'^commentsapi/(?P<pk>\d+)/$', views.CommentDetailSeri.as_view(), name='api_detail'),
    url(r'^commentsapi/(?P<pk>\d+)/update/$', views.CommentUpdateSeri.as_view(), name='api_update'),
    url(r'^commentsapi/(?P<pk>\d+)/delete/$', views.CommentDeleteSeri.as_view(), name='api_delete')

]
