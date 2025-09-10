from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, DeleteView, View, RedirectView
)

from conduit.articles.models import Article
from .comment_views import CommentCreateView


class Home(ListView):
    """View all published articles for the global feed."""

    template_name = "home.html"
    queryset = Article.objects.order_by("-created_at")
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["global_feed"] = Article.objects.order_by("-created_at")
        if self.request.user.is_authenticated:
            context["your_articles"] = self.request.user.profile.feed_articles()
        return context


class ArticleDetailView(DetailView):
    """Detail view for individual articles."""
    model = Article
    template_name = "article/article_detail.html"

    def get_object(self, **kwargs):
        slug_uuid = self.kwargs.get("slug_uuid")
        return get_object_or_404(Article, slug_uuid=slug_uuid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentCreateView().get_form_class()
        if self.request.user.is_authenticated:
            context["is_following"] = self.request.user.profile.is_following(self.object.author)
        return context


class ArticleCommentView(View):
    """View for viewing articles and posting comments."""

    def get(self, request, *args, **kwargs):
        view = ArticleDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentCreateView.as_view()
        return view(request, *args, **kwargs)


class EditorCreateView(LoginRequiredMixin, CreateView):
    """View for creating articles."""

    model = Article
    fields = ['title', 'description', 'body']
    template_name = "article/editor.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)

        self.object.author = self.request.user.profile
        self.object.save()
        return super().form_valid(form)


class EditorUpdateView(LoginRequiredMixin, UpdateView):
    """View for editing articles."""

    model = Article
    fields = ["title", "description", "body"]
    template_name = "article/editor.html"

    def get_object(self, **kwargs):
        slug_uuid = self.kwargs.get("slug_uuid")
        return get_object_or_404(Article, slug_uuid=slug_uuid)

    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().author.user:
            return super().post(request, *args, **kwargs)
        return redirect(self.get_object().get_absolute_url())


class EditorDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting articles."""

    template_name = "article/article_detail.html"
    success_url = reverse_lazy("home")

    def get_object(self, **kwargs):
        slug_uuid = self.kwargs.get("slug_uuid")
        return get_object_or_404(Article, slug_uuid=slug_uuid)

    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().author.user:
            return super().post(request, *args, **kwargs)
        return redirect(self.get_object().get_absolute_url())


class ArticleFavoriteView(RedirectView):
    pattern_name = "article_detail"  # ???

    def get_redirect_url(self, *args, **kwargs):
        url = self.request.POST.get("next", None)
        if url:
            return url
        else:
            return super().get_redirect_url(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        slug_uuid = self.kwargs.get("slug_uuid", None)
        article = get_object_or_404(Article, slug_uuid=slug_uuid)
        if request.user.profile.has_favorited(article):
            request.user.profile.unfavorite(article)
        else:
            request.user.profile.favorite(article)
        return super().post(request, *args, **kwargs)
