from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count
from django.http import Http404

from blog.models import Post, Category, Comment
from blog.forms import PostForm, CommentForm
from blog.constants import MAX_POSTS_PER_PAGE
from blog.mixins import PostMixin, CommentMixin


User = get_user_model()


def filter_posts(objects):
    return objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).select_related("author", "location", "category")


def get_page_obj(items_to_paginate, request):
    paginator = Paginator(items_to_paginate, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


@login_required
def index(request):
    template = "blog/index.html"
    posts = filter_posts(
        Post.objects.annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
    )
    page_obj = get_page_obj(posts, request)
    context = {"page_obj": page_obj}

    return render(request, template, context)


@login_required
def post_detail(request, post_id):
    template = "blog/detail.html"
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author and any(
            (
                post.pub_date > timezone.now(),
                not post.is_published,
                not post.category.is_published,
            )
    ):
        raise Http404
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post_id).select_related('post')
    context = {"post": post, "form": form, "comments": comments}

    return render(request, template, context)


@login_required
def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = filter_posts(category.posts)
    page_obj = get_page_obj(post_list, request)
    context = {"category": category, "page_obj": page_obj}

    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile",
            kwargs={"username": self.request.user}
        )


class PostUpdateView(PostMixin, LoginRequiredMixin, UpdateView):
    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail",
            kwargs={"post_id": self.object.pk}
        )


class PostDeleteView(PostMixin, LoginRequiredMixin, DeleteView):
    success_url = reverse_lazy("blog:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        context['object'] = post
        return context


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    post_instance = None
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        post_instance = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        form.instance.author = self.request.user
        form.instance.post = post_instance
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs.get("post_id")}
        )


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):
    pass


def user_profile(request, username):
    template = "blog/profile.html"
    profile = get_object_or_404(User, username=username)
    posts = profile.posts.annotate(comment_count=Count("comments")).order_by(
        "-pub_date"
    )
    if request.user.username != username:
        posts = posts.filter(is_published=True)
    page_obj = get_page_obj(posts, request)
    context = {"page_obj": page_obj, "profile": profile}

    return render(request, template, context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "blog/user.html"
    fields = ["username", "first_name", "last_name", "email"]

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )
