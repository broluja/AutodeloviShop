from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('getModels/', views.get_models, name='get_models'),
    path('autodelovi/', views.show_model, name='show_model'),
    path('checkout/', views.check_out, name='check_out'),
    path('order/', views.order, name='order'),
    path('about/', views.about, name='about'),
    path('ask-for-parts/', views.check_for_part, name='ask_for_parts'),
    path('brand/<str:model>/', views.open_model, name="open_model"),
    path('dynamic-search/', views.dynamic_search, name="dynamic_search"),
    path('part-search/', views.search_parts, name="search_parts"),
]

admin.site.site_header = 'Autodelovi Administration'
admin.site.index_title = 'Overview'
