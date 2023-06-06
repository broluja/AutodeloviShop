svetlosna_oprema = ("far", "maglenka", "migavac", "lampa", "katadiopter", "svetlo")
branik = ("branik", "spojler", "lajsna", "resetka", "nosac", "sina", "pvc", "maska")
limarija = ("hauba", "krilo", "lim", "brava", "kvaka")
zastitne_plastike = ("potkrilo", "zastita")
hladnjaci = ("ventilator", "hladnjak", "grejac")
retrovizori = ("retrovizor", "staklo", )
amortizeri = ("amortizer", )


def get_parts_by_categories(category: str) -> tuple:
    if category == "svetlosna oprema":
        return svetlosna_oprema
    elif category == "branik":
        return branik
    elif category ==  "limarija":
        return limarija
    elif category == "zaštitne plastike":
        return zastitne_plastike
    elif category == "hladnjaci":
        return hladnjaci
    elif category == "retrovizori":
        return retrovizori
    elif category == "amortizeri":
        return  amortizeri
