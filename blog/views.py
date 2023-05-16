from django.shortcuts import render

from .models import Post


def read_post(request, slug):
    post = Post.objects.get(slug=slug)
    context = {"post": post}
    post.views += 1
    post.save()
    return render(request, "blog-template.html", context=context)
