from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

class ProductWebsiteIn(BaseModel):
    element_id: str | None = None
    title: str | None = None
    img: str | None = None
    link_product: str | None = None
    link_website: str | None = None
    number_of_rating: str | None = None
    price: str | None = None
    rating: str | None = None
    shipping: str | None = None