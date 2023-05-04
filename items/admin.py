from django.contrib import admin
from .models import Item, Brand


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "gbg_id", "views", "orders"]
    list_per_page = 20
    list_display_links = ["__str__", "gbg_id"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "brand_id"]
    list_per_page = 400
    list_display_links = ["name", ]
