from django.urls import path

from .views import ArticleDetailView, Home

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("article/<slug:slug_uuid>", ArticleDetailView.as_view(), name="article_detail"),
]
