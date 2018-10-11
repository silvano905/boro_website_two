from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views.generic import TemplateView, DeleteView, DetailView, CreateView, UpdateView, ListView
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import MakePostForm
from .models import MakePost, LikeUserList
from comments.models import Comment
from .serializers import PostListSerializer, PostDetailSerializer, PostUpdateSerializer, PostCreateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from accounts.pagination import PostLimitOffsetPagination
from notify.signals import notify
from django.contrib.auth import get_user_model
from django.http import Http404
User = get_user_model()


class PostListSeri(ListAPIView, LoginRequiredMixin):
    serializer_class = PostListSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'info']  # to use this write (?search=)
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = MakePost.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(Q(info__icontains=query) |
                                                 Q(title__icontains=query)).distinct()
        return queryset_list


class PostDetailSeri(RetrieveAPIView, LoginRequiredMixin):
    queryset = MakePost.objects.all()
    serializer_class = PostDetailSerializer


class PostUpdateSeri(RetrieveUpdateAPIView, LoginRequiredMixin):
    queryset = MakePost.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PostDeleteSeri(DestroyAPIView, LoginRequiredMixin):
    queryset = MakePost.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class PostCreateAPIView(CreateAPIView, LoginRequiredMixin):
    queryset = MakePost.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@login_required
def crate_post(request):
    form = MakePostForm()

    if request.method == "POST":
        form = MakePostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            user_post = form.save(commit=False)
            user_post.author = request.user
            form.save(commit=True)
            return redirect('posts:list')
        else:
            form = MakePostForm()

    return render(request, 'posts/makepost_form.html', {'form': form})


@login_required
def post_details(request, pk):
    post = get_object_or_404(MakePost, pk=pk)
    is_liked = False

    if LikeUserList.objects.filter(user=request.user, post=post.pk):
        is_liked = True
    context = {
        'comment_list': Comment.objects.all().order_by('-created_date'),
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def like_post(request):
    is_liked = False
    post = get_object_or_404(MakePost, id=request.POST.get('post_id'))
    membership = LikeUserList.objects.filter(user=request.user, post=post.pk)
    if membership:
        membership.delete()
        is_liked = False

    else:
        notify.send(sender=request.user, actor=request.user, recipient=post.author, verb="liked your post: ' {a} '. ".format(a=post.title),
                    nf_type='followed_by_one_user')

        LikeUserList.objects.create(user=request.user, post=post)
        is_liked = True
    return redirect(post.get_absolute_url())


class PostUpdateView(UpdateView, LoginRequiredMixin):
    form_class = MakePostForm
    success_url = reverse_lazy('posts:postlist')
    model = MakePost


class PostDeleteView(DeleteView, LoginRequiredMixin):
    model = MakePost
    success_url = reverse_lazy('posts:list')


class UserPosts(ListView, LoginRequiredMixin):

    context_object_name = 'post_list'
    model = MakePost
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


@login_required
def post_list_search(request):

    queryset_list = MakePost.objects.all()

    query = request.GET.get('q')
    if query is not None:
        queryset_list = queryset_list.filter(Q(title__icontains=query) | Q(info__icontains=query))

    paginator = Paginator(queryset_list, 6)    # Show 25 contacts per page

    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    context = {
        "post_list": queryset
    }
    return render(request, 'posts/post_list.html', context)