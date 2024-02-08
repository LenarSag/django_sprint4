from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy

from blog.models import Post, Comment


class PostMixin:
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Post, pk=kwargs.get("post_id"), author=request.user)
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("comment_id"))
        if self.request.user != comment.author:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "blog:post_detail", kwargs={"post_id": self.kwargs.get("post_id")}
        )
