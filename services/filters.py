from sqlalchemy.orm import Query
from schemas import ParsedQuery
from models import Product

def apply_filters(query: Query, parsed: ParsedQuery) -> Query:
    if parsed.category:
        query = query.filter(Product.category == parsed.category)

    if parsed.style:
        query = query.filter(Product.style == parsed.style)

    if parsed.color:
        query = query.filter(Product.color == parsed.color)

    if parsed.gender:
        query = query.filter(Product.gender == parsed.gender)

    if parsed.brand:
        query = query.filter(Product.brand == parsed.brand)

    if parsed.material:
        query = query.filter(Product.material == parsed.material)

    if parsed.size:
        query = query.filter(Product.size == parsed.size)

    if parsed.min_price is not None:
        query = query.filter(Product.price >= parsed.min_price)

    if parsed.max_price is not None:
        query = query.filter(Product.price <= parsed.max_price)

    return query