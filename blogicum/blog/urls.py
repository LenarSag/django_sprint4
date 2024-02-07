from django.urls import path

from . import views


app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<int:id>/", views.post_detail, name="post_detail"),
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),
    path("posts/create/", views.create_post, name="create_post"),
    path("posts/edit/", views.create_post, name="edit_post"),
    path("posts/delete/", views.delete_post, name="delete_post"),
    path(
        "category/<slug:category_slug>/",
        views.category_posts,
        name="category_posts",
    ),
    path("profile/<slug:username>/", views.profile_view, name="profile"),
]
