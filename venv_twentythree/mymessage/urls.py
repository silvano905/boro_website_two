from django.conf.urls import url
from mymessage import views

app_name = 'mymessage'

urlpatterns = [
    url(r'^add_message_to/(?P<pk>\d+)/$', views.make_a_message, name='add_message'),
]