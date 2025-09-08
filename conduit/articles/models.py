import uuid

from django.db import models
from django.shortcuts import reverse


class Article(models.Model):
    """Article model."""

    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField(max_length=2000)
    body = models.TextField()
    author = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    slug_uuid = models.SlugField(max_length=100, editable=False, unique=True)
    uuid_field = models.UUIDField(default=uuid.uuid4, editable=False)

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug_uuid": self.slug_uuid})

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
        to_field="slug_uuid",
    )
    body = models.TextField()
    author = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:60] + "..."

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug_uuid": self.article.slug_uuid})
