from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "subtitle", "tag_list", "date_created"]
    list_per_page = 20
    list_display_links = ["title", "subtitle"]
    list_filter = ["date_created", "title"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    @staticmethod
    def tag_list(obj):
        return ", ".join(o.name for o in obj.tags.all())
