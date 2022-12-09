from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import Http404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CommentSerializer
from .forms import BlogPostListSerializer

from .models import Post, Comment
from .forms import PostForm, CommentForm


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()



def post_list(request):
    posts = Post.objects.for_user(user=request.user)
    return Response(render(request, 'blog/post_list.html', {'posts': posts}))
    #return render(request, 'blog/post_list.html', {'posts': posts})


def post_add(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', id=post.id)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    return redirect('post_list')


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    if not post.is_publish() and not request.user.is_staff:
        raise Http404("Запись в блоге не найдена")
    return Response(render(request, 'blog/post_detail.html', {'post': post}))





@login_required
def post_edit(request, id=None):
    post = get_object_or_404(Post, id=id) if id else None

    if post and post.author != request.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.is_published:
                post.published_date = timezone.now()
            else:
                post.published_date = None
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {'form': form})


def post_update(request, id):
    post = get_object_or_404(Post, id=id) if id else None

    if post and post.author != request.user:
        return redirect('post_list')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {'form': form})


@login_required()
def post_publish(request, id):
    post = get_object_or_404(Post, id=id)
    post.publish()
    return redirect('post_detail', id=id)


def add_comment(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})
