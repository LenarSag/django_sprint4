from django.contrib import admin

from .models import Category, Location, Post


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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
