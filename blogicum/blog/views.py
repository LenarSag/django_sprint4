from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from blog.constants import MAX_POSTS_PER_PAGE


User = get_user_model()


def filter_posts(objects):
    return objects.filter(
        is_published=True, category__is_published=True, pub_date__lte=timezone.now()
    ).select_related("author", "location", "category")


@login_required
def index(request):
    template = "blog/index.html"
    posts = filter_posts(Post.objects)
    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    return render(request, template, context)


@login_required
def post_detail(request, id):
    template = "blog/detail.html"
    post = get_object_or_404(
        filter_posts(Post.objects),
        pk=id,
    )
    form = CommentForm()
    comments = Comment.objects.filter(post_id=id)
    context = {"post": post, "form": form, "comments": comments}

    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_list = filter_posts(category.posts)
    paginator = Paginator(post_list, MAX_POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"category": category, "page_obj": page_obj}

    return render(request, template, context)


class PostMixin:
    pass


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse_lazy("blog:profile", kwargs={"username": self.request.user})
        return reverse_lazy("blog:index")


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs["pk"], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("blog:profile", kwargs={"username": self.request.user})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/create.html"

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs["pk"], author=request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("blog:profile", kwargs={"username": self.request.user})


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"

    def dispatch(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs.get("post_id"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_instance
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.post_instance.pk}
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        instance = get_object_or_404(Comment, pk=kwargs.get("comment_id"))
        if request.user != instance.author:
            return redirect("blog:post_detail", self.kwargs.get("post_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs.get("post_id")}
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("comment_id"))
        if self.request.user != comment.author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs.get("post_id")}
        )


def user_profile(request, username):
    template = "blog/profile.html"
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile)
    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
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
