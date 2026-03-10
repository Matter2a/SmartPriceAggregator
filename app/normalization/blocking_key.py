

def make_blocking_key(norm_brand: str, norm_title: str, weight_grams: int | None):

    words = norm_title.split()
    first_word = words[0] if words else "no-title"

    brand_part = norm_brand or "no-brand"

    weight_part = str(weight_grams) if weight_grams else "no-weight"

    return f"{brand_part}_{first_word}_{weight_part}"