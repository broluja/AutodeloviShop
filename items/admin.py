from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "gbg_id", "views", "orders"]
    list_per_page = 20
    list_display_links = ["__str__", "gbg_id"]
