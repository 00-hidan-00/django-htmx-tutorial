from django.urls import path

from .views import (
    ArticleDetailView, EditorCreateView, Home, EditorUpdateView, EditorDeleteView
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("article/<slug:slug_uuid>", ArticleDetailView.as_view(), name="article_detail"),
    path("editor", EditorCreateView.as_view(), name="editor_create"),
    path("editor/<slug:slug_uuid>", EditorUpdateView.as_view(), name="editor_update"),
    path("editor/<slug:slug_uuid>/delete", EditorDeleteView.as_view(), name="editor_delete"),

]
