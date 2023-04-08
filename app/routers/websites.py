from fastapi import APIRouter

from ..db.db import database, Website, Product
from ..models.product_website import ProductWebsiteIn

router = APIRouter()
##https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

@router.get("/websites/get", tags=["websites"])
async def read_websites():
    get_all_data = await Website.objects.all()
    print(get_all_data)
    return get_all_data

##get data website using parameters by filters
@router.get("/websites/get/{id}", tags=["websites"])
async def read_websites_id(id: int):
    try:
        get_all_data = await Website.objects.get(id=id)
        print(get_all_data)
        return get_all_data
    except:
        return {"error": "404: item not found"}

@router.get("/websites/get/name/{name}", tags=["websites"])
async def read_websites_name(name: str):
    try:
        return await Website.objects.get(name=name)
    except:
        return {"error": "404: item not found"}
        

@router.get("/websites/get/url/{url}", tags=["websites"])
async def read_websites_url(url: str):
    try:
        return await Website.objects.get(base_url=url)
    except:
        return {"error": "404: item not found"}

@router.get("/websites/get/category/{category}", tags=["websites"])
async def read_websites_url(category: str):
    try:
        return await Website.objects.get(category=category)
    except:
        return {"error": "404: item not found"}

@router.get("/websites/get/domain/{domain}", tags=["websites"])
async def read_websites_url(domain: str):
    try:
        return await Website.objects.get(domain=domain)
    except:
        return {"error": "404: item not found"}

@router.post("/websites/add", tags=["websites"])
async def add_website_product(product: ProductWebsiteIn):
    try:
        print(product)
        new_product = await Product.objects.create(**product.dict())
        return new_product
    except Exception as e:
        print(e)
        return {"error": "404: item not found"}