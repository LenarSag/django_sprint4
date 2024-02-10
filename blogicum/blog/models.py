from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedAndCreatedModel
from blog.constants import MAX_LENGTH_CHARFIELD


User = get_user_model()


class Category(PublishedAndCreatedModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGTH_CHARFIELD)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы "
            "латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Location(PublishedAndCreatedModel):
    name = models.CharField("Название места", max_length=MAX_LENGTH_CHARFIELD)

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self) -> str:
        return self.name


class Post(PublishedAndCreatedModel):
    title = models.CharField("Заголовок", max_length=MAX_LENGTH_CHARFIELD)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Категория",
    )

    image = models.ImageField("Картинка", blank=True)

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    text = models.TextField("Текст комментария", max_length=140)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return self.text
