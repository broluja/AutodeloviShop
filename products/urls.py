from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('getModels', views.get_models, name='get_models'),
    path('autodelovi', views.show_model, name='show_model'),
]
