from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    CreateView, DeleteView
)

from conduit.articles.models import Article, Comment


class CommentCreateView(LoginRequiredMixin, CreateView):
    """View for creating comments."""

    model = Comment
    fields = ["body"]
    template_name = "article/article_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        form.instance.article = Article.objects.filter(
            slug_uuid=self.kwargs.get("slug_uuid")
        ).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("article_detail", kwargs={"slug_uuid": self.object.article.slug_uuid})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting comments."""

    model = Comment
    template_name = "article/article_detail.html"

    def get_success_url(self):
        return reverse("article_detail", kwargs={"slug_uuid": self.object.article.slug_uuid})

    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().author.user:
            return super().post(request, *args, **kwargs)
        return redirect(self.get_object().get_absolute_url())
