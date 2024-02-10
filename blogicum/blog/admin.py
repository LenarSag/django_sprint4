from django.contrib import admin

from blog.models import Category, Location, Post, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "is_published",
        "created_at",
    )
    list_editable = (
        "description",
        "is_published",
    )
    list_display_links = ("title",)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_published",
        "created_at",
    )
    list_editable = ("is_published",)
    list_display_links = ("name",)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pub_date",
        "author",
        "category",
        "is_published",
    )
    list_editable = (
        "category",
        "is_published",
    )
    list_display_links = ("title",)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'post',
        'author',
    )
    list_editable = ('text',)
    list_display_links = ('author',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
