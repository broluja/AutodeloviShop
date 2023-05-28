from items.models import Item

group_one = ("hauba", "makaze", "blatobran", "branik", "amortizer haube", "haube")
group_two = ("blatobran", "potkrilo", "far", "nosac", "nosaca")
group_three = ("prednji branik", "vezni lim", "sina branika", "resetka", "maglenka", "maska", "branika")
group_four = ("far", "drzac fara", "okvir fara", "fara")
group_five = ("zadnji branik", "sina branika", "nosac branika", "branika")
group_six = ("stop lampa", "katadiopter", "svetlo tablice", "tablice")
group_seven = ("hladnjak vode", "hladnjak klime", "hladnjak interkulera", "hladnjak motora", "hladnjak")
part_groups = [group_one, group_two, group_three, group_four, group_five, group_six, group_seven]


def get_group_of_connected_parts(part_description):
    group_of_terms = []
    for group in part_groups:
        for element in group:
            if element in part_description:
                group_of_terms.extend(group[:-1])
    return set(group_of_terms)


def add_views(gbg_id):
    item = Item.objects.filter(gbg_id=gbg_id).first()
    if not item:
        item = Item.objects.create(gbg_id=gbg_id)
    else:
        item.views += 1
        item.save()
    return item
