import re 
def remove_weight_from_title(title: str) -> str:
    if not title:
        return ""
    
    pattern = r"\d+(?:[.,]\d+)?\s?(?:kg|кг|g|г)"
    title = re.sub(pattern, "", title, flags=re.I)
    title = re.sub(r"\s+", " ", title)
    return title.strip()