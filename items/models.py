from django.db import models


class Item(models.Model):
    gbg_id = models.CharField(max_length=100)
    views = models.PositiveIntegerField(default=1)
    orders = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return f"gbgID: {self.gbg_id}"
