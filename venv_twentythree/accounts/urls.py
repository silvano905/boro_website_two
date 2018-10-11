from django.conf.urls import url, include
from accounts import views


app_name = 'accounts'

urlpatterns = [
    url(r'^profile_block/$', views.block_user, name='block_user'),
    url(r'^$', views.create_user_form, name='registration'),
    url(r'^list/$', views.search_users, name='list'),
    url(r'^profile/$', views.edit_profile, name='profile'),
    url(r'^craeateprofile$', views.crate_user_profile, name='createprofile'),
    url(r'^list/(?P<pk>\d+)/$', views.user_detail_view, name='detail'),
    url(r'^list_messages/(?P<pk>\d+)/$', views.user_detail_messages_view, name='detail_messages'),
    url(r'^viewprofile/$', views.UserProfileView.as_view(), name='viewprofile'),
    url(r'^confirm-deactivate/$', views.ConfirmDeactivate.as_view(), name='confirm-deactivate'),
    url(r'^deactivate/$', views.delete_profile, name='deactivate'),
    url(r'^accountsapi/$', views.UsersListAPI.as_view()),
    url(r'^accountsapi/(?P<pk>\d+)/$', views.UsersDetailAPI.as_view(), name='api_detail'),
    url(r'^acoountsapi/(?P<pk>\d+)/update/$', views.UserUpdateAPI.as_view(), name='api_update'),

]