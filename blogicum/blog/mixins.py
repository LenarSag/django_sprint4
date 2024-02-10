from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy

from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("post_id"))
        if self.request.user != post.author:
            return redirect('blog:post_detail', self.kwargs.get("post_id"))
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"
    comment_id_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        if self.comment_id_kwarg in kwargs:
            comment = get_object_or_404(
                Comment,
                pk=kwargs.get(self.comment_id_kwarg)
            )
            if self.request.user != comment.author:
                raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs.get("post_id")}
        )
