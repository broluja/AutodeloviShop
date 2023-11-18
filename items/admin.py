from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Item, Brand


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "views", "orders", "open_item"]
    list_per_page = 20
    list_display_links = ["__str__", ]
    ordering = ("-orders", )

    def open_item(self, obj):
        return mark_safe(  # Creating link to the Item page
            f'<a target="_blank" href="{reverse("item:product_details", args=(obj.gbg_id,))}">product: {obj.gbg_id}</a>'
        )

    open_item.short_description = 'visit item'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "brand_id"]
    list_per_page = 400
    list_display_links = ["name", ]
