from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("<slug>/", views.read_post, name="read_post")
]
