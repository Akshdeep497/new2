from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    uniq_id: str
    title: str
    brand: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    categories: List[str] = []
    images: List[str] = []
    manufacturer: Optional[str] = None
    package_dimensions: Optional[str] = None
    country_of_origin: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None

class RecommendRequest(BaseModel):
    query: str
    k: int = 8

class RecommendItem(BaseModel):
    product: Product
    score: float

class RecommendResponse(BaseModel):
    items: List[RecommendItem]
