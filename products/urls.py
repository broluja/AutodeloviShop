from django.urls import path
from django.contrib import admin

from . import views


urlpatterns = [
    path("getModels/", views.get_models, name="get_models"),
    path("autodelovi/", views.show_model, name='show_model'),
    path("order", views.order, name="order"),
    path("brand/<str:brand>/", views.show_models, name="open_model"),
    path("part-search/", views.search_parts, name="search_parts"),
    path("parts/oem/", views.search_on_mobile, name="search_oem")
]

htmx_urlpatterns = [
    path("ask-for-parts/", views.check_for_part, name="ask_for_parts"),
    path("options/", views.get_options, name="get_options"),
    path("add-car/", views.add_car, name="add_car"),
    path("clear/", views.clear, name="clear"),
    path("dynamic-search/", views.dynamic_search, name="dynamic_search"),
    path("cart-addition/<str:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart-removal/", views.remove_from_cart, name="remove_from_cart"),
    path("quick-view/<str:product_id>/", views.quick_view, name="quick_view")
]

urlpatterns += htmx_urlpatterns
admin.site.site_header = "Autodelovi Administration"
admin.site.index_title = "Overview"
