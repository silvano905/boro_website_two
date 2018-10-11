from django.contrib import admin
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls import url, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('berenise90silvano90/', admin.site.urls),
    url(r'^notifications/', include('notify.urls', 'notifications')),
    url(r'^noti/', include('noti.urls', 'noti')),

    url(r'^group_message/', include('message_group.urls', namespace='group_message')),
    url(r'^friends/', include('friends.urls', namespace='friends')),
    url(r'^message/', include('mymessage.urls', namespace='message')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^todo/', include('todolist.urls', namespace='todo')),
    url(r'^login/$', LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    url(r'^$', views.index_home.as_view(), name='home'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
