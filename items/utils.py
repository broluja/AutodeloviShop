from items.models import Item


def add_views(gbg_id):
    item = Item.objects.filter(gbg_id=gbg_id).first()
    if not item:
        item = Item.objects.create(gbg_id=gbg_id)
    else:
        item.views += 1
        item.save()
    return item