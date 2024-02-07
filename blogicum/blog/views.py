from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Post, Category, User
from .forms import PostForm
from blog.constants import MAX_POSTS_PER_PAGE


@login_required
def add_comment(request, pk):
    # Получаем объект дня рождения или выбрасываем 404 ошибку.
    post = get_object_or_404(Post, pk=pk)
    # Функция должна обрабатывать только POST-запросы.
    form = PostForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        comment = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        comment.author = request.user
        # В поле birthday передаём объект дня рождения.
        comment.post = post
        # Сохраняем объект в БД.
        comment.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect("blog:index")


def filter_posts(objects):
    return objects.filter(
        is_published=True, category__is_published=True, pub_date__lte=timezone.now()
    ).select_related("author", "location", "category")


def index(request):
    template = "blog/index.html"
    posts = Post.objects.all()
    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, template, context)


def post_detail(request, id):
    template = "blog/detail.html"
    post = get_object_or_404(
        filter_posts(Post.objects),
        pk=id,
    )
    context = {"post": post}
    return render(request, template, context)


def create_post(request, pk=None):
    template = "blog/create.html"

    if pk is not None:
        instance = get_object_or_404(Post, pk=pk)
    else:
        instance = None

    form = PostForm(request.POST or None, instance=instance)
    context = {"form": form}
    if form.is_valid():
        form.save()

    return render(request, template, context)


def delete_post(request, pk):
    template = "blog/create.html"
    instance = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=instance)
    context = {"form": form}
    if request.method == "POST":
        instance.delete()
        return redirect("blog:index")
    return render(request, template, context)


# def create_post(request):
#     template = "blog/create.html"

#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#     else:
#         form = PostForm()
#     context = {"form": form}

#     return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_list = filter_posts(category.posts)
    context = {"category": category, "post_list": post_list}

    return render(request, template, context)


def profile_view(request, username):
    template = "blog/profile.html"
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile)
    paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"profile": profile, "page_obj": page_obj}

    return render(request, template, context)
