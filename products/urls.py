from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('getModels', views.get_models, name='get_models'),
    path('autodelovi', views.show_model, name='show_model'),
    path('product/<str:product_id>', views.product_details, name='product_details'),
    path('checkout', views.check_out, name='check_out'),
    path('order', views.order, name='order'),
    path('about', views.about, name='about'),
    path('ask-for-parts/<str:item>/<str:part>', views.order_parts, name='ask_for_parts'),
    path('open-model/<str:model>', views.open_model, name="open_model"),
    path('open-model-parts', views.show_model_parts, name='model_parts')
]
