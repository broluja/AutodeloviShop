from django.urls import path
from django.contrib import admin
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('getModels/', views.get_models, name='get_models'),
    path('autodelovi/', views.show_model, name='show_model'),
    path('product/<str:product_id>/', views.product_details, name='product_details'),
    path('checkout/', views.check_out, name='check_out'),
    path('order/', views.order, name='order'),
    path('about/', views.about, name='about'),
    path('ask-for-parts/', views.check_for_part, name='ask_for_parts'),
    path('brand/<str:model>/', views.open_model, name="open_model"),
]

admin.site.site_header = 'Autodelovi Administration'
admin.site.index_title = 'Overview'
