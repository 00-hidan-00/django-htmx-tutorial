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
