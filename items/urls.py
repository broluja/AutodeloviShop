from django.urls import path

from . import views

app_name = 'item'
urlpatterns = [
    path('<str:product_id>/', views.product_details, name='product_details'),
]
