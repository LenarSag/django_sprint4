from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post, Category, User
from blog.constants import MAX_VISIBLE_POSTS


def filter_posts(objects):
    return objects.filter(
        is_published=True, category__is_published=True, pub_date__lte=timezone.now()
    ).select_related("author", "location", "category")


def index(request):
    template = "blog/index.html"
    post_list = filter_posts(Post.objects)[:MAX_VISIBLE_POSTS]
    context = {"post_list": post_list}
    return render(request, template, context)


def post_detail(request, id):
    template = "blog/detail.html"
    post = get_object_or_404(
        filter_posts(Post.objects),
        pk=id,
    )
    context = {"post": post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_list = filter_posts(category.posts)
    context = {"category": category, "post_list": post_list}
    return render(request, template, context)


def profile_view(request, username):
    template = "blog/profile.html"
    profile = User.objects.get(username=username)
    context = {"profile": profile}
    return render(request, template, context)
