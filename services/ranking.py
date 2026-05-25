from schemas import ParsedQuery

def calculate_score(product, parsed: ParsedQuery) -> float:
    score = 0.0

    if parsed.category and product.category == parsed.category:
        score += 3.0

    if parsed.style and product.style == parsed.style:
        score += 2.0

    if parsed.color and product.color == parsed.color:
        score += 2.0

    if parsed.gender and product.gender == parsed.gender:
        score += 1.5

    if parsed.brand and product.brand == parsed.brand:
        score += 2.5

    if parsed.max_price is not None and product.price <= parsed.max_price:
        score += 1.0

    if parsed.min_price is not None and product.price >= parsed.min_price:
        score += 1.0

    return score


def sort_products(products, parsed: ParsedQuery, sort_by: str):
    enriched = []
    for product in products:
        score = calculate_score(product, parsed)
        setattr(product, "score", score)
        enriched.append(product)

    if sort_by == "price_asc":
        return sorted(enriched, key=lambda x: x.price)

    if sort_by == "price_desc":
        return sorted(enriched, key=lambda x: x.price, reverse=True)

    if sort_by == "brand":
        return sorted(enriched, key=lambda x: (x.brand or "").lower())

    return sorted(enriched, key=lambda x: getattr(x, "score", 0), reverse=True)