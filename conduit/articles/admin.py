from django.contrib import admin

from .models import Article


class ArticleAdmin(admin.ModelAdmin):  # new
    readonly_fields = ("slug_uuid", "uuid_field")


admin.site.register(Article, ArticleAdmin)
