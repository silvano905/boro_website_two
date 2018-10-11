from django.conf.urls import url
from posts import views


app_name = 'posts'

urlpatterns = [
    url(r'^$', views.post_list_search, name='list'),
    url(r'^create_post/$', views.crate_post, name='create_post'),
    url(r'^by/(?P<username>[-\w]+)/$', views.UserPosts.as_view(), name='for_user'),
    # url(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='single'),

    # url(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.PostUpdateView.as_view(), name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.PostDeleteView.as_view(), name='post_remove'),

    url(r'^post/(?P<pk>\d+)$', views.post_details, name='post_detail'),
    url(r'^like/$', views.like_post, name='like_post'),

    url(r'^postsapi/$', views.PostListSeri.as_view()),
    url(r'^postsapi/create/$', views.PostCreateAPIView.as_view()),
    url(r'^postsapi/(?P<pk>\d+)/$', views.PostDetailSeri.as_view(), name='api_detail'),
    url(r'^postsapi/(?P<pk>\d+)/update/$', views.PostUpdateSeri.as_view(), name='api_update'),
    url(r'^postsapi/(?P<pk>\d+)/delete/$', views.PostDeleteSeri.as_view(), name='api_delete')
]