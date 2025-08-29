from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView
)

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


class EditorCreateView(CreateView):
    """View for creating articles."""

    model = Article
    fields = ['title', 'description', 'body']
    template_name = "editor.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.author = self.request.user.profile
        self.object.save()
        return super().form_valid(form)


class EditorUpdateView(UpdateView):
    """View for editing articles."""

    model = Article
    fields = ["title", "description", "body"]
    template_name = "editor.html"

    def get_object(self, **kwargs):
        slug_uuid = self.kwargs.get("slug_uuid")
        return get_object_or_404(Article, slug_uuid=slug_uuid)


class EditorDeleteView(DeleteView):
    """View for deleting articles."""

    template_name = "article_detail.html"
    success_url = reverse_lazy("home")

    def get_object(self, **kwargs):
        slug_uuid = self.kwargs.get("slug_uuid")
        return get_object_or_404(Article, slug_uuid=slug_uuid)
