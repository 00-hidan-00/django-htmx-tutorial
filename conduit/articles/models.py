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

    def get_absolute_url(self):  # new
        return reverse("article_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
