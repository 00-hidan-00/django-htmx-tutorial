from django.urls import path

from .views import (
    ArticleCommentView,
    ArticleFavoriteView,
    EditorCreateView,
    Home,
    EditorUpdateView,
    EditorDeleteView,
    CommentDeleteView,

)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("feed", Home.as_view(), name="home_feed"),
    path("article/<slug:slug_uuid>", ArticleCommentView.as_view(), name="article_detail"),
    path("editor", EditorCreateView.as_view(), name="editor_create"),
    path("editor/<slug:slug_uuid>", EditorUpdateView.as_view(), name="editor_update"),
    path("editor/<slug:slug_uuid>/delete", EditorDeleteView.as_view(), name="editor_delete"),
    path("article/<slug:slug_uuid>/comment/<int:pk>/delete", CommentDeleteView.as_view(), name="comment_delete"),
    path("article/<slug:slug_uuid>/favorite", ArticleFavoriteView.as_view(), name="article_favorite"),





]
