from typing import Optional, List
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    sort_by: Optional[str] = "relevance"   # relevance, price_asc, price_desc, brand
    limit: Optional[int] = 20


class ParsedQuery(BaseModel):
    category: Optional[str] = None
    style: Optional[str] = None
    color: Optional[str] = None
    gender: Optional[str] = None
    brand: Optional[str] = None
    material: Optional[str] = None
    size: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None


class ProductOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    brand: Optional[str]
    category: Optional[str]
    style: Optional[str]
    color: Optional[str]
    gender: Optional[str]
    size: Optional[str]
    material: Optional[str]
    price: float
    store: Optional[str]
    image_url: Optional[str]
    product_url: Optional[str]
    score: Optional[float] = None

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    parsed_query: ParsedQuery
    results: List[ProductOut]