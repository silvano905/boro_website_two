from django.shortcuts import render
from .forms import CommentForm, SuggestionForm
from .models import Comment
from django.shortcuts import render, get_object_or_404, redirect
from posts.models import MakePost
from .permissions import IsOwnerOrReadOnly
from todolist.models import Todo
from .serializers import CommentListSerializer, CommentDetailSerializer, CommentUpdateSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from notify.signals import notify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(MakePost, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post     # Remember here that our Comment object has an attribute called post of type Post
            comment.author = request.user
            comment.save()

            notify.send(sender=request.user, actor=request.user, recipient=post.author,
                        verb="added a comment to your post: ' {} ' ".format(post.title), nf_type='followed_by_one_user')

            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'comments/comment_form.html', {'form': form})


@login_required
def add_suggestion_to_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.todo = todo    # Remember here that our Comment object has an attribute called post of type Post
            suggestion.author = request.user
            suggestion.save()

            notify.send(sender=request.user, actor=request.user, recipient=todo.user,
                        verb="added a suggestion to your wish: ' {} ' ".format(todo.title), nf_type='followed_by_one_user')

            return redirect('todo:single', username=todo.user.username, pk=todo.pk)
    else:
        form = SuggestionForm()

    return render(request, 'comments/suggestion_form.html', {'form': form})


# ------------------API--------------------------------------------------------------------

class CommentListAPI(ListAPIView, LoginRequiredMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [IsAuthenticated]


class CommentDetailSeri(RetrieveAPIView, LoginRequiredMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


class CommentUpdateSeri(RetrieveUpdateAPIView, LoginRequiredMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated]


class CommentDeleteSeri(DestroyAPIView, LoginRequiredMixin):
    queryset = MakePost.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

