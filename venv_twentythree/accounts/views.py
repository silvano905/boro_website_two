from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView, DetailView, CreateView, UpdateView, ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .forms import UserFormRegistration, UserFormProfile, UserFormCreationFormUpdate, UserFormProfileUpdate
from .models import Profile, BlockedList
from posts.models import MakePost
from todolist.models import Todo
from mymessage.models import MyMessage
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from .serializers import UsersListSerializer, UsersDetailSerializer, UserUpdateSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter
from .pagination import PostLimitOffsetPagination
from itertools import chain
from notify.models import Notification

from operator import attrgetter
# class UsersListAPI(ListAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = UsersListSerializer
#     permission_classes = [IsAuthenticated]


class UsersListAPI(ListAPIView, LoginRequiredMixin):
    serializer_class = UsersListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['description', 'gender', 'user']  # to use this write (?gender= or ?user= or ?q=)
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Profile.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(Q(description__icontains=query) |
                                                 Q(gender__icontains=query) |
                                                 Q(user__last_name__icontains=query) |
                                                 Q(user__email__icontains=query) |
                                                 Q(user__first_name__icontains=query) |
                                                 Q(user__username__icontains=query)).distinct()
        return queryset_list


class UsersDetailAPI(RetrieveAPIView, LoginRequiredMixin):
    queryset = Profile.objects.all()
    serializer_class = UsersDetailSerializer


class UserUpdateAPI(RetrieveUpdateAPIView, LoginRequiredMixin):
    queryset = Profile.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

# ------------------------------------Views------------------------------------------------------


# @login_required
# def index_home(request):
#     posts = MakePost.objects.all()
#     metas = Todo.objects.all()
#
#     # both_lists = list(chain(posts, metas))
#     # paginator = Paginator(both_lists, 8)
#     # page = request.GET.get('page')
#     # pagination_list = paginator.get_page(page)
#
#     context = {
#         'post_list': posts,
#         'meta_list': metas,
#
#     }
#     return render(request, 'main.html', context)


class index_home(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = MakePost.objects.all()
        context['meta_list'] = Todo.objects.all()
        context['notifications_list'] = Notification.objects.filter(deleted=False, recipient=self.request.user)
        return context

    def get_queryset(self):
        return MakePost.objects.all()


class ViewUserProfile(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/profile.html'


def crate_user_profile(request):
    form = UserFormProfile()

    if request.method == "POST":
        form = UserFormProfile(data=request.POST, files=request.FILES)

        if form.is_valid():
            userprofile = form.save(commit=False)

            pic = form.cleaned_data['profile_pic']
            if not pic:
                userprofile.profile_pic = 'hummingbird.jpg'
            userprofile.user = request.user
            form.save(commit=True)

            return render(request, 'main.html')
        else:
            form = UserFormProfile()

    return render(request, 'accounts/profile.html', {'form': form})


def create_user_form(request):
    form = UserFormRegistration()

    if request.method == "POST":
        form = UserFormRegistration(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return render(request, 'main.html')
        else:
            form = UserFormRegistration()

    return render(request, 'registration/form.html', {'form': form})


@login_required
def search_users(request):
    queryset_list = {}

    query = request.GET.get('q')
    if query is not None:
        queryset_list = Profile.objects.all().exclude(user=request.user)
        queryset_list = queryset_list.filter(
            Q(user__first_name=query) | Q(user__username=query) | Q(user__last_name=query) | Q(user__email=query))

    context = {
        "object_list": queryset_list
    }
    return render(request, 'search_users/index.html', context)


@login_required
def user_detail_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    is_blocked = False

    if BlockedList.objects.filter(user=profile.user, profile=request.user.profiles):
        is_blocked = True
    context = {
        'user_list': profile,
        'is_blocked': is_blocked,
        'post_list': MakePost.objects.filter(author=profile.user),
        'todo_list': Todo.objects.filter(user=profile.user),
        'messages_list': MyMessage.objects.all().order_by('created_date')
    }
    return render(request, 'accounts/user_detail.html', context)


@login_required
def user_detail_messages_view(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    search_user = MyMessage.objects.filter(author=profile.user, recipient=request.user.profiles)
    request_user = MyMessage.objects.filter(author=request.user, recipient=profile)

    is_blocked = False

    if BlockedList.objects.filter(user=profile.user, profile=request.user.profiles):
        is_blocked = True

    result_list = sorted(
        chain(search_user, request_user),
        key=lambda instance: instance.created_date)

    context = {
        'is_blocked': is_blocked,
        'user_list': profile,
        'both_lists': result_list
    }
    return render(request, 'accounts/user_detail_messages.html', context)


@login_required
def edit_profile(request):
    image = request.user.profiles.profile_pic

    if request.method == 'POST':
        form1 = UserFormCreationFormUpdate(request.POST, instance=request.user)
        form2 = UserFormProfileUpdate(request.POST, request.FILES, instance=request.user.profiles)

        if form1.is_valid() and form2.is_valid():
            form1.save(commit=True)
            form2.save(commit=True)
            return redirect('home')
    else:
        form1 = UserFormCreationFormUpdate(instance=request.user)
        form2 = UserFormProfileUpdate(instance=request.user.profiles)


    return render(request, 'accounts/createprofile.html', {'form': form1, 'formm': form2, 'image': image})


class UserProfileView(TemplateView, LoginRequiredMixin):
    template_name = 'accounts/view_profile.html'


class ConfirmDeactivate(TemplateView, LoginRequiredMixin):
    template_name = 'profile/confirm_deactivate.html'


@login_required
def delete_profile(request):
    user = request.user
    user.is_active = False
    user.save()
    messages.success(request, 'Profile successfully disabled.')
    return redirect('home')


@login_required
def block_user(request):
    profile = get_object_or_404(Profile, pk=request.POST.get('post_id'))
    member = BlockedList.objects.filter(user=profile.user, profile=request.user.profiles)
    if member:
        member.delete()

    else:
        BlockedList.objects.create(user=profile.user, profile=request.user.profiles)
    return redirect(profile.get_absolute_url())