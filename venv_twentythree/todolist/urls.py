from django.conf.urls import url, include
from . import views

app_name = 'todolist'

urlpatterns = [
    url(r'^$', views.world_todo_list, name='todo_list'),
    url(r'^my_todo$', views.addTodo, name='add'),
    url(r'^complete/(?P<pk>\d+)/$', views.complete_todo, name='complete'),
    url(r'^delete_complete/$', views.delete_completed, name='deletecomplete'),
    url(r'^delete_all/$', views.delete_all, name='deleteall'),
    url(r'^by/(?P<username>[-\w]+)/$', views.UserTodo.as_view(), name='for_user'),
    url(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.TodoDetailView.as_view(), name='single'),
    url(r'^remove/(?P<pk>\d+)/$', views.delete_individual_todo, name='remove_todo_individual'),


]