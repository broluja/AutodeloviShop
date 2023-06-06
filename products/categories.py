svetlosna_oprema = ("far", "maglenka", "migavac", "lampa", "katadiopter", "svetlo")
branik = ("branik", "spojler", "lajsna", "resetka", "nosac", "sina", "pvc", "maska")
limarija = ("hauba", "krilo", "lim", "brava", "kvaka")
zastitne_plastike = ("potkrilo", "zastita")
hladnjaci = ("ventilator", "hladnjak", "grejac")
retrovizori = ("retrovizor", "staklo", )
amortizeri = ("amortizer", )


def get_parts_by_categories(category: str) -> tuple:
    match category:
        case "svetlosna oprema":
            return svetlosna_oprema
        case "branik":
            return branik
        case "limarija":
            return limarija
        case "zaštitne plastike":
            return zastitne_plastike
        case "hladnjaci":
            return hladnjaci
        case "retrovizori":
            return retrovizori
        case "amortizeri":
            return  amortizeri
