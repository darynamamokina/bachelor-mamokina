from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Product
from schemas import SearchRequest, SearchResponse, ProductOut

from services.parser import parse_user_query
from services.filters import apply_filters
from services.ranking import sort_products
from services.embedding_search import semantic_rank_products
from services.hybrid_search import hybrid_rank_products


router = APIRouter(
    prefix="/search",
    tags=["search"]
)


@router.post("/", response_model=SearchResponse)
def search_products(
    payload: SearchRequest,
    db: Session = Depends(get_db)
):
    parsed = parse_user_query(payload.query)

    query = db.query(Product)

    query = apply_filters(query, parsed)

    products = query.all()

    # semantic
    if payload.sort_by == "semantic":
        ranked_products = semantic_rank_products(
            payload.query,
            products
        )

    # hybrid
    elif payload.sort_by == "hybrid":
        ranked_products = hybrid_rank_products(
            payload.query,
            products,
            parsed
        )

    # default
    else:
        ranked_products = sort_products(
            products,
            parsed,
            payload.sort_by
        )

    ranked_products = ranked_products[:payload.limit]

    return SearchResponse(
        parsed_query=parsed,
        results=[
            ProductOut.model_validate(product)
            for product in ranked_products
        ]
    )


@router.get("/all", response_model=list[ProductOut])
def get_all_products(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    return [
        ProductOut.model_validate(product)
        for product in products
    ]