import re
from schemas import ParsedQuery


CATEGORY_KEYWORDS = {
    # сукня
    "сукня": "dress",
    "сукні": "dress",
    "сукню": "dress",
    "сукнею": "dress",

    "плаття": "dress",
    "плаття": "dress",

    # худі
    "худі": "hoodie",
    "худі": "hoodie",

    "кофта": "hoodie",
    "кофти": "hoodie",
    "кофту": "hoodie",

    # футболка
    "футболка": "tshirt",
    "футболки": "tshirt",
    "футболку": "tshirt",

    # сорочка
    "сорочка": "shirt",
    "сорочки": "shirt",
    "сорочку": "shirt",

    # штани
    "штани": "pants",
    "штанів": "pants",
    "штанами": "pants",

    # джинси
    "джинси": "jeans",
    "джинсів": "jeans",
    "джинсами": "jeans",

    # куртка
    "куртка": "jacket",
    "куртки": "jacket",
    "куртку": "jacket",

    # пальто
    "пальто": "coat",
}

STYLE_KEYWORDS = {
    "кежуал": "casual",
    "casual": "casual",

    "повсякденний": "casual",
    "повсякденна": "casual",
    "повсякденні": "casual",
    "повсякденне": "casual",

    # зручний / комфортний стиль
    "зручний": "casual",
    "зручна": "casual",
    "зручне": "casual",
    "зручні": "casual",
    "зручно": "casual",

    "комфортний": "casual",
    "комфортна": "casual",
    "комфортне": "casual",
    "комфортні": "casual",
    "комфортно": "casual",

    "легкий": "casual",
    "легка": "casual",
    "легке": "casual",
    "легкі": "casual",

    "на кожен день": "casual",
    "щоденний": "casual",
    "щоденна": "casual",
    "щоденне": "casual",
    "щоденні": "casual",

    "для прогулянки": "casual",
    "для навчання": "casual",
    "для університету": "casual",
    "для роботи": "casual",

    "спортивний": "sport",
    "спортивна": "sport",
    "спортивне": "sport",
    "спортивні": "sport",

    "елегантний": "elegant",
    "елегантна": "elegant",
    "елегантні": "elegant",
    "елегантне": "elegant",

    "вечір": "elegant",
    "вечірня": "elegant",
    "вечірній": "elegant",
    "вечірнє": "elegant",
    "вечірні": "elegant",
    "вечірніх": "elegant",
    "вечора": "elegant",
    "на вечір": "elegant",
    "для вечора": "elegant",

    "свято": "elegant",
    "святковий": "elegant",
    "святкова": "elegant",
    "святкове": "elegant",
    "святкові": "elegant",

    "класичний": "classic",
    "класичні": "classic",
    "класична": "classic",
    "класичне": "classic",

    "oversize": "oversize",
    "оверсайз": "oversize",
}

COLOR_KEYWORDS = {
    # чорний
    "чорний": "black",
    "чорна": "black",
    "чорне": "black",
    "чорні": "black",
    "чорного": "black",
    "чорну": "black",

    # білий
    "білий": "white",
    "біла": "white",
    "біле": "white",
    "білі": "white",
    "білого": "white",

    # червоний
    "червоний": "red",
    "червона": "red",
    "червоне": "red",
    "червоні": "red",
    "червоного": "red",

    # синій
    "синій": "blue",
    "синя": "blue",
    "синє": "blue",
    "сині": "blue",
    "синього": "blue",

    # зелений
    "зелений": "green",
    "зелена": "green",
    "зелене": "green",
    "зеленого": "green",

    # сірий
    "сірий": "gray",
    "сіра": "gray",
    "сіре": "gray",
    "сірого": "gray",

    # бежевий
    "бежевий": "beige",
    "бежева": "beige",
    "бежеве": "beige",
    "бежевого": "beige",
}

GENDER_KEYWORDS = {
     # жіночий
    "жіноча": "female",
    "жіночий": "female",
    "жіноче": "female",
    "жіночі": "female",
    "жіночого": "female",
    "жіночу": "female",
    "для жінок": "female",

    # чоловічий
    "чоловіча": "male",
    "чоловічий": "male",
    "чоловіче": "male",
    "чоловічі": "male",
    "чоловічого": "male",
    "чоловічу": "male",
    "для чоловіків": "male",

    "унісекс": "unisex",
}

MATERIAL_KEYWORDS = {
    "бавовна": "cotton",
    "бавовняний": "cotton",
    "бавовняна": "cotton",

    "поліестер": "polyester",
    "синтетика": "polyester",

    "вовна": "wool",
    "вовняний": "wool",

    "льон": "linen",
    "лляний": "linen",

    "джинс": "denim",
    "денім": "denim",
}

SIZE_KEYWORDS = {
    "xs": "XS",
    "s": "S",
    "m": "M",
    "l": "L",
    "xl": "XL",
}

def extract_price_range(text: str):
    text = text.lower()

    under_match = re.search(r"(до|не дорожче|максимум)\s+(\d+)", text)
    if under_match:
        return None, float(under_match.group(2))

    from_to_match = re.search(r"від\s+(\d+)\s+до\s+(\d+)", text)
    if from_to_match:
        return float(from_to_match.group(1)), float(from_to_match.group(2))

    above_match = re.search(r"(від|дорожче)\s+(\d+)", text)
    if above_match:
        return float(above_match.group(2)), None

    return None, None


def find_keyword(text: str, mapping: dict):
    for key, value in mapping.items():
        if key in text:
            return value
    return None


def parse_user_query(query: str) -> ParsedQuery:
    text = query.lower()

    min_price, max_price = extract_price_range(text)

    category = find_keyword(text, CATEGORY_KEYWORDS)
    style = find_keyword(text, STYLE_KEYWORDS)
    color = find_keyword(text, COLOR_KEYWORDS)
    gender = find_keyword(text, GENDER_KEYWORDS)
    material = find_keyword(text, MATERIAL_KEYWORDS)
    size = find_keyword(text, SIZE_KEYWORDS)

    # Якщо користувач шукає сукню і стать явно не вказана,
    # автоматично вважаємо товар жіночим
    if category == "dress" and gender is None:
        gender = "female"

    return ParsedQuery(
        category=category,
        style=style,
        color=color,
        gender=gender,
        material=material,
        size=size,
        min_price=min_price,
        max_price=max_price,
    )