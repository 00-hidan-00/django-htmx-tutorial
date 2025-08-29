from django.views.generic import ListView

from .models import Article


class Home(ListView):
    """View all published articles for the global feed."""

    template_name = "home.html"
    queryset = Article.objects.order_by("-created_at")
    context_object_name = "articles"
