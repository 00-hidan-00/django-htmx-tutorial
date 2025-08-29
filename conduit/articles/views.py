from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Article


class Home(ListView):
    """View all published articles for the global feed."""

    template_name = "home.html"
    queryset = Article.objects.order_by("-created_at")
    context_object_name = "articles"


class ArticleDetailView(DetailView):
    """Detail view for individual articles."""
    model = Article
    template_name = "article_detail.html"

    def get_object(self, **kwargs):
        slug_uuid = self.kwargs.get("slug_uuid")
        return get_object_or_404(Article, slug_uuid=slug_uuid)
