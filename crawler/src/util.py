
ASKO_DESCRIPTION_KEYS = ("konstrukce", "potah", "rozměry", "výška sedáku")
VENETI_DESCRIPTION_KEYS = ("konstrukce", "potah", "rozměry", "výška sedáku")
BELIANI_DESCRIPTION_KEYS = ("konstrukce", "potah", "rozměry", "výška sedáku")

def init_data_map() -> dict:
    return {
        "length": 0,
        "width": 0,
        "depth": 0,
        "cover_material": "BLANK",
        "sit_height": 0,
        "contains_metal": -1,
        "contains_hardwood": -1,
        "price": 0
    }
