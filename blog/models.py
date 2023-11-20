from PIL import Image

from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager


class Post(models.Model):
    """Post model representing a page content on blog page."""
    title = models.CharField(max_length=99)
    subtitle = models.CharField(max_length=99)
    content = models.TextField()
    conclusion = models.TextField()
    views = models.PositiveIntegerField(default=1)
    slug = models.SlugField(default=None, blank=True, null=True, unique=True)
    image = models.ImageField(default='default.jpg', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    objects = models.Manager()
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        """Resizing image on post save."""
        super().save()
        if self.slug is None:
            value = self.subtitle
            self.slug = slugify(value[:50])
            self.save()

        img = Image.open(self.image.path)
        width, height = img.size  # Get dimensions

        if width > 300 and height > 300:
            # keep ratio but shrink down
            img.thumbnail((width, height))
            width, height = img.size

            # check, which one is smaller
            if height < width:
                # make square by cutting off equal amounts left and right
                left = (width - height) // 2
                right = (width + height) // 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))
            elif width < height:
                # make square by cutting off bottom
                left = 0
                right = width
                top = 0
                bottom = width
                img = img.crop((left, top, right, bottom))
            img.thumbnail((300, 300))
            img.save(self.image.path)

        elif width > 300 and height == 300:
            left = (width - 300) // 2
            right = (width + 300) // 2
            top = 0
            bottom = 300
            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

        elif width > 300 > height:
            left = (width - height) // 2
            right = (width + height) // 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

        elif width < 300 < height:
            # most potential for disaster
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

        elif width < 300 and height < 300:
            if height < width:
                left = (width - height) // 2
                right = (width + height) // 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))
            elif width < height:
                height = width
                left = 0
                right = width
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))
            img.save(self.image.path)
        elif width == 300 and height > 300:
            # potential for disaster
            left = 0
            right = 300
            top = 0
            bottom = 300
            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

        elif width == 300 and height < 300:
            left = (width - height) // 2
            right = (width + height) // 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

        elif width < 300 and height == 300:
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

        elif width and height == 300:
            img.save(self.image.path)
